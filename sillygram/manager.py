import asyncio

from aiogram import Bot as AiogramBot
from aiogram.types import (
    InlineKeyboardMarkup,
    Message as AiogramMessage,
    InlineKeyboardButton,
)

from .ui import SillyPage

from .context import PATH
from .text import SillyText
from .data import SillyDefaults, Data
from .user import SillyUser
from .events import SillyEvent
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple

TIME_DELTA = 0.2
MAX_TIME = 120


class SillyManager:
    _aiogram_bot: AiogramBot
    _data: Data

    @property
    def registry(self):
        return self._data.global_registry

    @property
    def users(self):
        return self._data.users

    @property
    def stats(self):
        return SillyText(self._data.stats.get_report())

    @property
    def settings(self):
        return self._data.settings

    @property
    def privileges_names(self):
        return self._data.privileges.all_names

    def set_privilege(self, user: SillyUser, privilege_name: Optional[str]):
        self._data.users.set_privilege(user.id, privilege_name)

    # region High-level messaging methods

    # region Target message

    async def show_page(
        self,
        user: SillyUser,
        page_name: Any,
        new_target_message=False,
        not_found_message: Optional[SillyText] = None,
        f_args: Optional[Tuple] = None,
        f_kwargs: Optional[Dict[str, Any]] = None,
    ):
        page = self._data.pages.get(page_name)

        if not page:
            if not not_found_message:
                not_found_message = self._data.settings.labels.page_not_found

            await self.show_notice(user, not_found_message)
            return

        format_args = await page.get_format_args(
            self, SillyEvent(user, *(f_args or ()), **(f_kwargs or {}))
        )

        @SillyManager.privileged(page.privileged if page.privileged else None)
        async def _(manager: SillyManager, event: SillyEvent):
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

        await _(self, SillyEvent(user))

    async def refresh_page(
        self,
        user: SillyUser,
        not_found_message: Optional[SillyText] = None,
        f_args: Optional[Tuple] = None,
        f_kwargs: Optional[Dict[str, Any]] = None,
    ):
        await self.show_page(
            user,
            self._data.get_current_page_name(user.id),
            not_found_message=not_found_message,
            f_args=f_args,
            f_kwargs=f_kwargs,
        )

    async def restore_page(
        self,
        user: SillyUser,
        not_found_message: Optional[SillyText] = None,
        f_args: Optional[Tuple] = None,
        f_kwargs: Optional[Dict[str, Any]] = None,
    ):
        page: Optional[SillyPage] = None

        try:
            page = self._data.pages.get(self._data.get_current_page_name(user.id))

            if not page:
                if not not_found_message:
                    not_found_message = self._data.settings.labels.page_not_found

                await self.show_notice(user, not_found_message)
                await self.show_page(user, SillyDefaults.Names.Pages.HOME)
                return

        except Exception:
            await self.show_page(user, SillyDefaults.Names.Pages.HOME)
            return

        @SillyManager.privileged(page.privileged if page.privileged else False)
        async def _(manager: SillyManager, event: SillyEvent):
            format_args: Optional[Tuple[str, ...]] = None

            format_args = self._data.get_format_args(user.id)
            if len(format_args) == 0:
                format_args = (
                    *(f_args or ()),
                    *(f_kwargs.values() if f_kwargs else ()),
                )

            await self._edit_target_message(
                user,
                page.text.format(*format_args if format_args else ()).localize(
                    user.language_code
                ),
                page.keyboard(user.language_code),
            )

            self._data.set_format_args(user.id, format_args)

        await _(self, SillyEvent(user))

    async def _ask_for_restore(self, user: SillyUser):
        self._data.io.push_to_add(user.id)

    async def _prevent_restore(self, user: SillyUser):
        self._data.io.push_to_delete(user.id)

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

            await self._ask_for_restore(user)
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
        page = self._data.pages.get(current_page_name)

        if page is None:
            page = self._data.pages.get(SillyDefaults.Names.Pages.HOME)
            if page is None:
                return

        await self._delete_target_message(user)
        await self._aiogram_bot.send_message(user.id, text.localize(user.language_code))

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

            await self._ask_for_restore(user)

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
                elif "message to edit not found" in str(e):
                    await self._send_new_target_message(user, text, keyboard)
                elif "message not modified" in str(e):
                    ...
                elif "message is not modified" in str(e):
                    ...
                else:
                    raise

        await self._prevent_restore(user)

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

        await self._prevent_restore(user)

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
    def privileged(value: bool | str = True):
        def decorator(handler: Callable[[SillyManager, SillyEvent], Awaitable[None]]):
            async def wrapper(manager: SillyManager, event: SillyEvent):
                if value:
                    privilege = manager._data.privileges.master
                    if isinstance(value, str):
                        actual_privilege = manager._data.privileges[value]
                        if actual_privilege:
                            privilege = actual_privilege
                    if not manager._data.privileges.matches(event.user, privilege.name):
                        message = (
                            privilege.message
                            if privilege.message is not None
                            else manager._data.settings.labels.access_denied
                        )
                        return await manager.show_popup(event.user, message)

                return await handler(manager, event)

            return wrapper

        return decorator

    # endregion

    def __init__(self, aiogram_bot: AiogramBot, data: Data):
        self._aiogram_bot = aiogram_bot
        self._data = data
