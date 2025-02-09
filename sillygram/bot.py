import asyncio
import logging
from datetime import time, timedelta
from typing import Optional, Sequence, Callable, Awaitable, Any

from aiogram import Bot as AiogramBot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InaccessibleMessage
from aiogram.methods import DeleteWebhook

from .context import PATH

from .data.logger import SillyLogger

from .data import SillySettings
from .events import SillyEvent, SillyErrorEvent
from .manager import SillyManager
from .data import Data, SillyDefaults
from .ui import SillyPage, SillyActionButton

from .activities import SillyRegularActivity, SillyDateTimeActivity
from .controls import controls_pages


class SillyBot:
    """
    Core class for a SillyGram bot.
    Create an instance of this class with all neccessary settings
    and use the 'launch' method to start the bot.
    """

    _aiogram_bot: AiogramBot
    _dispatcher: Dispatcher

    _data: Data
    _manager: SillyManager
    _logger: SillyLogger

    _regular_activities: Sequence[SillyRegularActivity]

    # region Startup & shutdown

    async def _on_aiogram_startup(self):
        await self._data.stats.summarize_hourly_statistics(self._manager)
        await self._data.stats.summarize_daily_statistics(self._manager)
        await self._data.stats.summarize_monthly_statistics(self._manager)
        await self._data.stats.summarize_yearly_statistics(self._manager)

        if self._data.settings.on_startup:
            asyncio.create_task(self._data.settings.on_startup(self._manager))  # type: ignore
        if self._regular_activities:
            asyncio.create_task(self._scheduling_loop())

        self._data.io.start_loop()

    async def _on_aiogram_shutdown(self):
        if self._data.settings.on_shutdown:
            asyncio.create_task(self._data.settings.on_shutdown(self._manager))  # type: ignore

    def launch(self):
        """
        Use this method to start the bot asynchronously. It must be called from synchronous code.

        After this method is called, the program goes into an endless loop,
        and the thread will be blocked until the bot is terminated. Therefore, all the settings must be up
        before the SillyBot is launched.
        """

        asyncio.run(self._launch())

    async def _launch(self):
        """
        Use this method to start the bot. It must be called from asynchronous code.

        After this method is called, the program goes into an endless loop,
        and the thread will be blocked until the bot is terminated. Therefore, all the settings must be up
        before the SillyBot is launched.
        """
        if self._data.settings.skip_updates:
            await self._aiogram_bot(DeleteWebhook(drop_pending_updates=True))

        await self._dispatcher.start_polling(self._aiogram_bot, skip_updates=True)

    # endregion

    # region Events handlers

    def _setup_handlers(self):
        self._dispatcher.callback_query.register(
            self._on_close_button_clicked,
            F.data.startswith(SillyDefaults.CallbackData.CLOSE),
        )

        self._dispatcher.callback_query.register(
            self._on_continue_button_clicked,
            F.data.startswith(SillyDefaults.CallbackData.CONTINUE),
        )

        self._dispatcher.callback_query.register(
            self._on_return_button_clicked,
            F.data.startswith(SillyDefaults.CallbackData.BACK),
        )

        self._dispatcher.callback_query.register(
            self._on_cancel_button_clicked,
            F.data.startswith(SillyDefaults.CallbackData.CANCEL),
        )

        self._dispatcher.callback_query.register(
            self._on_dialog_option_clicked,
            F.data.startswith(SillyDefaults.CallbackData.OPTION_TEMPLATE),
        )

        self._register_command(SillyDefaults.Commands.HOME, self._on_home)
        self._register_command(SillyDefaults.Commands.START, self._on_start)
        self._register_command(SillyDefaults.Commands.CONTROLS, self._on_configure)

        self._dispatcher.message.register(self._on_text_input, F.text)
        self._dispatcher.message.register(self._on_other_input)

        pages = (self._data.pages.get(name) for name in self._data.pages.names)
        buttons = []
        for page in pages:
            if page is None:
                raise KeyError("Page not found")
            for button in page.buttons:
                if button not in buttons:
                    buttons.append(button)

        for button in buttons:
            if isinstance(button, SillyActionButton):
                self._register_callback(button.identity, button.on_click)

        self._dispatcher.callback_query.register(self._default_callback_handler)

    def _register_command(self, command: str, handler: Any):
        async def aiogram_handler(message: Message):
            if not message.from_user:
                return

            user = self._manager.users.get(self._data.indicate(message.from_user))

            if user is None:
                return
            if user.is_banned:
                return

            result = None

            try:
                event = SillyEvent(user)
                result = await handler(self._manager, event)

            except Exception as e:
                result = await self._on_error(
                    self._manager, SillyErrorEvent(user, exception=e)
                )

            try:
                await message.delete()
            except Exception:
                ...

            return result

        self._dispatcher.message.register(aiogram_handler, Command(command))

    def _register_callback(self, callback_identity: str, handler: Any):
        async def aiogram_handler(callback: CallbackQuery):
            await callback.answer()

            user = self._manager.users.get(self._data.indicate(callback.from_user))

            if user is None:
                return
            if user.is_banned:
                return

            try:
                event = SillyEvent(user)
                return await handler(self._manager, event)
            except Exception as e:
                await self._on_error(self._manager, SillyErrorEvent(user, exception=e))

        self._dispatcher.callback_query.register(
            aiogram_handler, F.data.startswith(callback_identity)
        )

    # region Default handlers

    async def _on_error(self, manager: SillyManager, event: SillyErrorEvent):
        await manager.show_popup(
            event.user, self._data.settings.labels.error.format(str(event.exception))
        )

    async def _on_start(self, manager: SillyManager, event: SillyEvent):
        await manager.show_page(
            event.user, SillyDefaults.Names.Pages.START, new_target_message=True
        )

    async def _on_home(self, manager: SillyManager, event: SillyEvent):
        await manager.show_page(
            event.user, SillyDefaults.Names.Pages.HOME, new_target_message=True
        )

    @staticmethod
    @SillyManager.priveleged()
    async def _on_configure(manager: SillyManager, event: SillyEvent):
        await manager.show_page(event.user, SillyDefaults.Names.Pages.CONTROLS)

    async def _on_text_input(self, message: Message):
        if not message.from_user:
            return
        user = self._manager.users.get(self._data.indicate(message.from_user))

        if not user:
            return
        if user.is_banned:
            return

        try:
            await message.delete()
        except Exception:
            ...

        self._data.io.push_text(
            message.from_user.id, message.text if message.text else ""
        )

    async def _on_other_input(self, message: Message):
        if not message.from_user:
            return

        user = self._manager.users.get(self._data.indicate(message.from_user))

        if not user:
            return
        if user.is_banned:
            return

        try:
            await message.delete()
        except Exception:
            ...

    async def _on_dialog_option_clicked(self, callback: CallbackQuery):
        await callback.answer()

        user = self._manager.users.get(self._data.indicate(callback.from_user))

        if not user:
            return

        if user.is_banned:
            return

        option = 0

        if not self._data.io.is_dialog_listening(user.id):
            await self._manager.restore_page(user)

        if callback.data:
            if callback.data == SillyDefaults.CallbackData.CANCEL_OPTION:
                option = -1
            else:
                if not self._data.io.is_dialog_listening(user.id):
                    await self._manager.show_notice(
                        user, self._data.settings.labels.try_again
                    )
                option = int(
                    callback.data.replace(
                        SillyDefaults.CallbackData.OPTION_TEMPLATE, ""
                    )
                )

        self._data.io.push_dialog_result(callback.from_user.id, option)

    async def _on_close_button_clicked(self, callback: CallbackQuery):
        await callback.answer()
        user = self._manager.users.get(self._data.indicate(callback.from_user))

        if not user:
            return

        if user.is_banned:
            return

        try:
            if isinstance(callback.message, Message) and not isinstance(
                callback.message, InaccessibleMessage
            ):
                await callback.message.delete()
        except Exception:
            ...

    async def _on_continue_button_clicked(self, callback: CallbackQuery):
        await callback.answer()
        user = self._manager.users.get(self._data.indicate(callback.from_user))

        if not user:
            return

        if user.is_banned:
            return

        target_message_id = self._data.get_target_message_id(user.id)
        if target_message_id is None:
            return

        await self._aiogram_bot.edit_message_reply_markup(
            chat_id=user.id, message_id=target_message_id, reply_markup=None
        )

        await self._manager.show_page(
            user,
            self._data.get_current_page_name(callback.from_user.id),
            new_target_message=True,
        )

    async def _on_return_button_clicked(self, callback: CallbackQuery):
        await callback.answer()
        user = self._manager.users.get(self._data.indicate(callback.from_user))

        if not user:
            return

        if user.is_banned:
            return

        await self._manager.restore_page(user)

    async def _on_cancel_button_clicked(self, callback: CallbackQuery):
        await callback.answer()
        user = self._manager.users.get(self._data.indicate(callback.from_user))

        if not user:
            return

        if user.is_banned:
            return

        if not self._data.io.is_input_listening(user.id):
            await self._manager.restore_page(user)

        self._data.io.push_text(
            callback.from_user.id, SillyDefaults.CallbackData.INPUT_CANCEL_MARKER
        )
        self._data.io.stop_input_listening(callback.from_user.id)

    async def _default_callback_handler(self, callback: CallbackQuery):
        await callback.answer()

        user = self._manager.users.get(self._data.indicate(callback.from_user))

        if user is None:
            return
        if user.is_banned:
            return

        await self._manager.show_page(
            user, SillyDefaults.Names.Pages.HOME, new_target_message=True
        )

    # endregion

    # endregion

    # region Regular activites

    async def _scheduling_loop(self, time_delta: int = 20):
        while True:
            # logging.info("Checking for regular activities to run...")
            for scheduled_activity in self._regular_activities:
                await scheduled_activity.execute(self._manager)
            await asyncio.sleep(time_delta)

    def _setup_regular_activities(self):
        hourly_stats_activity = SillyDateTimeActivity(
            self._data.stats.summarize_hourly_statistics,
            times=tuple(time(hour=h) for h in range(24)),
            max_time_delta=timedelta(minutes=1),
        )

        daily_stats_activity = SillyDateTimeActivity(
            self._data.stats.summarize_daily_statistics,
            times=time(hour=0),
            max_time_delta=timedelta(minutes=1),
        )

        monthly_stats_activity = SillyDateTimeActivity(
            self._data.stats.summarize_monthly_statistics,
            times=time(hour=0),
            monthdays=1,
        )

        yearly_stats_activity = SillyDateTimeActivity(
            self._data.stats.summarize_yearly_statistics,
            times=time(hour=0),
            monthdays=1,
            months=1,
        )

        stats_activities = (
            hourly_stats_activity,
            daily_stats_activity,
            monthly_stats_activity,
            yearly_stats_activity,
        )

        self._regular_activities = (
            (*self._data.settings.regular_activities, *stats_activities)
            if self._data.settings.regular_activities
            else stats_activities
        )

    # endregion

    def __init__(
        self,
        token: str,
        pages: Optional[Sequence[SillyPage]] = None,
        settings: Optional[SillySettings] = None,
    ):
        """
        :param token: telegram-API token received from BotFather.
        :param pages: sequence of page objects to include. Names must be unique.
        :param settings: silly-bot settings. None means default settings.
        """

        settings = settings if settings else SillySettings()
        self._logger = SillyLogger(
            path=PATH / "logs",
            file_logging_mode=settings.file_logging_mode,
            console_logging_mode=settings.console_logging_mode,
        )
        pages = (*(pages or ()), *controls_pages)
        self._data = Data(settings if settings is not None else SillySettings(), *pages)
        self._aiogram_bot = AiogramBot(
            token=token, default=DefaultBotProperties(parse_mode="HTML")
        )
        self._dispatcher = Dispatcher()
        self._dispatcher.startup.register(self._on_aiogram_startup)
        self._dispatcher.shutdown.register(self._on_aiogram_shutdown)
        self._manager = SillyManager(self._aiogram_bot, self._data)
        self._data.init_users(self._manager)
        self._data.init_io(self._manager)

        self._setup_regular_activities()
        self._setup_handlers()
