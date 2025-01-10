import asyncio

from aiogram import Bot as AiogramBot
from aiogram.types import (
    InlineKeyboardMarkup,
    Message as AiogramMessage,
    InlineKeyboardButton,
)

from .privelege import SillyPrivelege

from .ui import SillyPage

from .context import PATH
from .text import SillyText
from .data import SillyDefaults, Data, SillyLogger
from .user import SillyUser
from .events import SillyEvent
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple

TIME_DELTA = 0.2
MAX_TIME = 120


class SillyManager:
    _aiogram_bot: AiogramBot
    _data: Data

    _logger: SillyLogger

    @property
    def registry(self):
        return self._data.registry

    @property
    def users(self):
        return self._data.users

    @property
    def stats(self):
        return SillyText(self._data.stats.get_report())

    # region High-level messaging methods

    # region Target message

    async def show_page(
        self,
        user: SillyUser,
        page_name: Any,
        new_target_message=False,
        f_args: Optional[Tuple] = None,
        f_kwargs: Optional[Dict[str, Any]] = None,
    ):
        page = self._data.pages.get(page_name)
        format_args = await page.get_format_args(
            self, SillyEvent(user, *(f_args or ()), **(f_kwargs or {}))
        )

        if new_target_message:
            await self._send_new_target_message(
                user,
                page.text.format(*format_args if format_args else ()).localize(
                    user.language_code
                ),
                page.keyboard(user.language_code),
            )
        else:
            await self._edit_target_message(
                user,
                page.text.format(*format_args if format_args else ()).localize(
                    user.language_code
                ),
                page.keyboard(user.language_code),
            )

        self._data.set_format_args(user.id, format_args)
        self._data.set_current_page_name(user.id, page_name)

    async def refresh_page(
        self,
        user: SillyUser,
        f_args: Optional[Tuple] = None,
        f_kwargs: Optional[Dict[str, Any]] = None,
    ):
        page: Optional[SillyPage] = None
        format_args: Optional[Tuple[str, ...]] = None

        try:
            page = self._data.pages.get(self._data.get_current_page_name(user.id))
            if f_args or f_kwargs:
                format_args = await page.get_format_args(
                    self, SillyEvent(user, *(f_args or ()), **(f_kwargs or {}))
                )

        except Exception:
            await self.show_page(user, SillyDefaults.Names.START_PAGE)
            return

        if format_args is None:
            format_args = self._data.get_format_args(user.id)

        await self._edit_target_message(
            user,
            page.text.format(*format_args if format_args else ()).localize(
                user.language_code
            ),
            page.keyboard(user.language_code),
        )

        self._data.set_format_args(user.id, format_args)

    async def show_dialog(
        self,
        user: SillyUser,
        question: SillyText,
        *dialog_options: SillyText,
        cancelable: bool = False,
    ) -> int | None:
        buttons = []
        row = []
        c = 0
        for i, text in enumerate(dialog_options):
            c += 1
            row.append(
                InlineKeyboardButton(
                    text=text.localize(user.language_code), callback_data=f"OPTION_{i}"
                )
            )

            if c >= 3:
                c = 0
                buttons.append(row)
                row = []

        if row:
            buttons.append(row)

        if cancelable:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=self._data.settings.labels.cancel.localize(
                            user.language_code
                        ),
                        callback_data=SillyDefaults.CallbackData.CANCEL_OPTION,
                    )
                ]
            )

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await self._edit_target_message(
            user, question.localize(user.language_code), keyboard=keyboard
        )

        async def wait_for_result():
            self._data.io.start_dialog_listening(user.id)
            option = None

            timer = 0

            while option is None:
                option = self._data.io.pop_dialog_result(user.id)

                timer += TIME_DELTA
                if timer > MAX_TIME:
                    self._data.io.stop_dialog_listening(user.id)
                    break

                await asyncio.sleep(TIME_DELTA)

            await self.refresh_page(user)
            return option if option != -1 else None

        return await asyncio.get_event_loop().create_task(wait_for_result())

    # endregion

    # region Additional messages

    async def show_popup(self, user: SillyUser, text: SillyText):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=self._data.settings.labels.go_back.localize(
                            user.language_code
                        ),
                        callback_data=SillyDefaults.CallbackData.BACK,
                    )
                ]
            ]
        )
        await self._edit_target_message(
            user, text.localize(user.language_code), keyboard
        )

    async def show_notice(self, user: SillyUser, text: SillyText):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=self._data.settings.labels.close.localize(
                            user.language_code
                        ),
                        callback_data=SillyDefaults.CallbackData.CLOSE,
                    )
                ]
            ]
        )
        await self._aiogram_bot.send_message(
            user.id, text.localize(user.language_code), reply_markup=keyboard
        )

    async def show_banner(self, user: SillyUser, text: SillyText):
        current_page_name = self._data.get_current_page_name(user.id)

        await self._delete_target_message(user)
        await self._aiogram_bot.send_message(user.id, text.localize(user.language_code))

        page = self._data.pages.get(current_page_name)
        await self._send_new_target_message(
            user,
            page.text.localize(user.language_code),
            keyboard=page.keyboard(user.language_code),
            separate=False,
        )

    # endregion

    # region User input

    async def get_input(self, user: SillyUser, prompt: SillyText) -> str | None:
        async def task():
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=self._data.settings.labels.cancel.localize(
                                user.language_code
                            ),
                            callback_data=SillyDefaults.CallbackData.CANCEL,
                        )
                    ]
                ]
            )

            await self._edit_target_message(
                user, prompt.localize(user.language_code), keyboard
            )
            self._data.io.start_input_listening(user.id)

            timer = 0

            text = None
            while text is None:
                text = self._data.io.pop_text(user.id)

                timer += TIME_DELTA
                if timer > MAX_TIME:
                    self._data.io.stop_input_listening(user.id)
                    break

                await asyncio.sleep(0.2)

            return (
                text if text != SillyDefaults.CallbackData.INPUT_CANCEL_MARKER else None
            )

        return await asyncio.get_event_loop().create_task(task())

    async def get_yes_no_answer(
        self, user: SillyUser, question: SillyText, cancelable: bool = False
    ) -> Optional[bool]:
        option = await self.show_dialog(
            user,
            question,
            self._data.settings.labels.no,
            self._data.settings.labels.yes,
            cancelable=cancelable,
        )
        if option is None:
            return None
        return True if option else False

    # endregion

    # # region Other

    # async def start_broadcast(
    #     self, text: SillyText, user_ids: Optional[List[int]] = None
    # ):
    #     async def _task(_text: SillyText, _user_ids: Optional[List[int]] = None):
    #         all_users = self._data.users.get_all()
    #         users = (
    #             all_users
    #             if user_ids is None
    #             else (user for user in all_users if user.id in user_ids)
    #         )

    #         for user in users:
    #             await self.show_notice_banner(user, _text)
    #             await asyncio.sleep(0.5)

    #     await asyncio.get_event_loop().create_task(_task(text, user_ids))

    # # endregion

    # endregion

    # region Low-level messaging methods

    async def _edit_target_message(
        self, user: SillyUser, text: str, keyboard: InlineKeyboardMarkup
    ):
        target_message_id = self._data.get_target_message_id(user.id)

        if target_message_id is None:
            await self._send_new_target_message(user, text, keyboard)
        else:
            try:
                await self._aiogram_bot.edit_message_text(
                    chat_id=user.id,
                    text=text,
                    message_id=target_message_id,
                    reply_markup=keyboard,
                )
            except Exception as e:
                # noqa: F841
                if "message can't be edited" in str(e):
                    await self._send_new_target_message(user, text, keyboard)
                elif "message not modified" in str(e):
                    ...
                elif "message is not modified" in str(e):
                    ...
                else:
                    raise

    async def _send_new_target_message(
        self,
        user: SillyUser,
        text: str,
        keyboard: InlineKeyboardMarkup,
        separate: bool = True,
    ):
        if separate:
            await self._send_separation_messages(user)

        message: AiogramMessage = await self._aiogram_bot.send_message(
            user.id, text, reply_markup=keyboard
        )
        self._data.set_target_message_id(user.id, message.message_id)

    async def _send_separation_messages(self, user: SillyUser):
        for i in range(0, 5):
            await self._aiogram_bot.send_message(
                user.id,
                text=self._data.settings.labels.emoji_separator.localize(
                    user.language_code
                ),
            )
            await asyncio.sleep(0.15)

    async def _replace_target_message(
        self, user: SillyUser, text: str, keyboard: InlineKeyboardMarkup
    ):
        target_message_id = self._data.get_target_message_id(user.id)
        if target_message_id is not None:
            try:
                await self._aiogram_bot.delete_message(user.id, target_message_id)
            except Exception as e:  # noqa: F841
                ...

        await self._send_new_target_message(user, text, keyboard)

    async def _delete_target_message(self, user: SillyUser):
        target_message_id = self._data.get_target_message_id(user.id)
        if target_message_id is None:
            return

        try:
            await self._aiogram_bot.delete_message(user.id, target_message_id)
        except Exception as e:  # noqa: F841
            pass

    # endregion

    # region Decorators

    @staticmethod
    def protected(privelege_name: Optional[str] = None):
        def decorator(handler: Callable[[SillyManager, SillyEvent], Awaitable[None]]):
            async def wrapper(manager: SillyManager, event: SillyEvent):
                privelege = (
                    manager._data.priveleges[privelege_name]
                    if privelege_name is not None
                    else manager._data.priveleges.master
                )
                if privelege:
                    if not manager._data.priveleges.matches(event.user, privelege.name):
                        message = (
                            privelege.message
                            if privelege.message is not None
                            else manager._data.settings.labels.access_denied
                        )
                        return await manager.show_popup(event.user, message)
                else:
                    return await manager.show_popup(event.user, manager._data.settings.labels.access_denied)
                
                return await handler(manager, event)

            return wrapper

        return decorator

    # endregion

    def __init__(self, aiogram_bot: AiogramBot, data: Data):
        self._aiogram_bot = aiogram_bot
        self._data = data

        self._logger = SillyLogger(PATH / "logs", self._data.settings.log_to_console)
