import asyncio
import logging
from typing import *

from aiogram import Bot as AiogramBot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.methods import DeleteWebhook

from .data import SillySettings
from .management import SillyEvent, SillyManager
from .data import Data, SillyDefaults
from .ui import Page, ActionButton


class SillyBot:
    _aiogram_bot: AiogramBot
    _dispatcher: Dispatcher

    _data: Data
    _manager: SillyManager
    
    # region Starting

    @staticmethod
    async def _on_startup():
        logging.info("SillyBot is polling...")

    def launch_async(self):
        """
        Use this method to start the bot asynchronously. It must be called from synchronous code.

        After this method is called, the program goes into an endless loop,
        and the thread will be blocked until the bot is terminated. Therefore, all the settings must be up
        before the SillyBot is launched.
        """

        asyncio.run(self.launch())

    async def launch(self):
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
        self._dispatcher.callback_query.register(self._on_close_button_clicked,
                                                 F.data.startswith(SillyDefaults.CallbackData.
                                                                   CLOSE))

        self._dispatcher.callback_query.register(self._on_continue_button_clicked,
                                                 F.data.startswith(SillyDefaults.CallbackData.
                                                                   CONTINUE))

        self._dispatcher.callback_query.register(self._on_return_button_clicked,
                                                 F.data.startswith(SillyDefaults.CallbackData.
                                                                   BACK))

        self._dispatcher.callback_query.register(self._on_cancel_button_clicked,
                                                 F.data.startswith(SillyDefaults.CallbackData.
                                                                   CANCEL))

        self._dispatcher.callback_query.register(self._on_dialog_option_clicked,
                                                 F.data.startswith(SillyDefaults.CallbackData.
                                                                   OPTION_TEMPLATE))

        self._register_command(SillyDefaults.Commands.HOME, self._on_home)
        self._register_command(SillyDefaults.Commands.START, self._on_start)

        self._dispatcher.message.register(self._on_text_input, F.text)
        self._dispatcher.message.register(self._on_other_input)

        pages = (self._data.pages.get(name) for name in self._data.pages.names)
        buttons = []
        for page in pages:
            for button in page.buttons:
                if button not in buttons:
                    buttons.append(button)

        for button in buttons:
            if isinstance(button, ActionButton):
                self._register_callback(button.identity, button.on_click)

    def _register_command(self, command: str, handler: Any):
        async def aiogram_handler(message: Message):
            try:
                await message.delete()
            except Exception:
                ...

            user_info = self._data.users.indicate(message.from_user)

            args = message.text.split()[1:]
            event = SillyEvent(user_info, *args)
            return await handler(self._manager, event)

        self._dispatcher.message.register(aiogram_handler, Command(command))

    def _register_callback(self, callback_identity: str, handler: Any):
        async def aiogram_handler(callback: CallbackQuery):
            user_info = self._data.users.indicate(callback.from_user)
            event = SillyEvent(user_info)
            return await handler(self._manager, event)

        self._dispatcher.callback_query.register(aiogram_handler, F.data.startswith(callback_identity))

    # region Default handlers

    async def _on_start(self, manager: SillyManager, event: SillyEvent):
        await manager.goto_page(event.user, SillyDefaults.Names.START_PAGE, new_target_message=True)

    async def _on_home(self, manager: SillyManager, event: SillyEvent):
        await manager.goto_page(event.user, SillyDefaults.Names.HOME_PAGE, new_target_message=True)

    async def _on_text_input(self, message: Message):
        try:
            await message.delete()
        except Exception:
            ...

        self._data.io.push_text(message.from_user.id, message.text)

    async def _on_other_input(self, message: Message):
        print(message)
        try:
            await message.delete()
        except Exception:
            ...

    async def _on_dialog_option_clicked(self, callback: CallbackQuery):
        self._data.users.indicate(callback.from_user)
        option = int(callback.data.replace(SillyDefaults.CallbackData.OPTION_TEMPLATE, ""))
        self._data.io.push_dialog_result(callback.from_user.id, option)

    async def _on_close_button_clicked(self, callback: CallbackQuery):
        self._data.users.indicate(callback.from_user)
        try:
            await callback.message.delete()
        except Exception:
            ...

    async def _on_continue_button_clicked(self, callback: CallbackQuery):
        user = self._data.users.indicate(callback.from_user)

        target_message_id = self._data.users.get_target_message_id(user.id)
        if target_message_id is None:
            return

        await self._aiogram_bot.edit_message_reply_markup(chat_id=user.id, message_id=target_message_id,
                                                          reply_markup=None)

        await self._manager.goto_page(user,
                                      self._data.users.get_current_page_name(callback.from_user.id),
                                      new_target_message=True)

    async def _on_return_button_clicked(self, callback: CallbackQuery):
        user = self._data.users.indicate(callback.from_user)
        await self._manager.refresh_page(user)

    async def _on_cancel_button_clicked(self, callback: CallbackQuery):
        user = self._data.users.indicate(callback.from_user)

        self._data.io.stop_listening(callback.from_user.id)
        await self._manager.refresh_page(user)

    # endregion

    # endregion

    def __init__(self, token: str, *pages: Page, settings: Optional[SillySettings] = None):
        """
        :param token: telegram-API token received from BotFather.
        :param pages: page objects to include. Names must be unique.
        :param settings: settings for bot. Leave empty for default settings.
        """

        self._data = Data(settings if settings is not None else SillySettings(), *pages)
        self._aiogram_bot = AiogramBot(token=token, default=DefaultBotProperties(parse_mode="HTML"))
        self._dispatcher = Dispatcher()
        self._dispatcher.startup.register(SillyBot._on_startup)
        self._manager = SillyManager(self._aiogram_bot, self._data)

        self._setup_handlers()
