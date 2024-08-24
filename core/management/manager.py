import asyncio

from aiogram import Bot as AiogramBot
from aiogram.types import InlineKeyboardMarkup, Message as AiogramMessage, InlineKeyboardButton

from silly_config import PATH
from utility import localize, SillyLogger
from ..data import SillyDefaults, Data, SillyUser
from typing import *


class SillyManager:
    _aiogram_bot: AiogramBot
    _data: Data

    _logger: SillyLogger

    @property
    def registry(self):
        return self._data.registry

    # region High-level messaging methods

    # region Target message

    async def goto_page(self, user: SillyUser, page_name: Any, new_target_message=False):
        page = self._data.pages.get(page_name)
        if new_target_message:
            await self._send_new_target_message(user, page.text[user.language_code],
                                                page.keyboard(user.language_code))
        else:
            await self._edit_target_message(user, page.text[user.language_code],
                                            page.keyboard(user.language_code))
        self._data.users.set_current_page_name(user.id, page_name)

    async def refresh_page(self, user: SillyUser):
        page = self._data.pages.get(self._data.users.get_current_page_name(user.id))
        await self._edit_target_message(user, page.text[user.language_code],
                                        page.keyboard(user.language_code))

    async def show_message(self, user: SillyUser, text: str | Dict[str | Sequence[str], str]):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=self._data.settings.labels.go_back,
                                                   callback_data=SillyDefaults.CallbackData.BACK)]]
        )
        await self._edit_target_message(user, localize(text, user.language_code), keyboard)

    async def show_dialog(self, user: SillyUser, question: str | Dict[str | Sequence[str], str],
                          *dialog_options: str | Dict[str | Sequence[str], str]) -> int | None:
        buttons = []
        row = []
        c = 0
        for i, text in enumerate(dialog_options):
            c += 1
            row.append(InlineKeyboardButton(text=localize(text, user.language_code), callback_data=f"OPTION_{i}"))

            if c >= 3:
                buttons.append(row)
                row = []

        if row:
            buttons.append(row)

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await self._edit_target_message(user, localize(question, user.language_code), keyboard=keyboard)

        async def wait_for_result():
            option = None
            while option is None:
                option = self._data.io.pop_dialog_result(user.id)
                await asyncio.sleep(0.2)

            return option

        return await asyncio.get_event_loop().create_task(wait_for_result())

    # endregion

    # region Additional messages

    async def show_notification(self, user: SillyUser, text: str | Dict[str | Sequence[str], str]):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=self._data.settings.labels.close,
                                                   callback_data=SillyDefaults.CallbackData.CLOSE)]]
        )
        await self._aiogram_bot.send_message(user.id, localize(text, user.language_code), reply_markup=keyboard)

    async def show_interruption(self, user: SillyUser, text: str | Dict[str | Sequence[str], str]):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=self._data.settings.labels.go_on,
                                                   callback_data=SillyDefaults.CallbackData.CONTINUE)]]
        )
        await self._edit_target_message(user, localize(text, user.language_code), keyboard)

    async def show_banner(self, user: SillyUser, text: str | Dict[str | Sequence[str], str]):
        current_page_name = self._data.users.get_current_page_name(user.id)

        await self._delete_target_message(user)
        await self._aiogram_bot.send_message(user.id, localize(text, user.language_code))

        page = self._data.pages.get(current_page_name)

        await self._send_new_target_message(user, localize(page.text, user.language_code),
                                            keyboard=page.keyboard(user.language_code), separate=False)

    # endregion

    # region User input

    async def get_input(self, user: SillyUser, prompt: str | Dict[str | Sequence[str], str]) -> str | None:
        async def task():
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text=self._data.settings.labels.cancel,
                                                       callback_data=SillyDefaults.CallbackData.CANCEL)]]
            )

            await self._edit_target_message(user, localize(prompt, user.language_code), keyboard)
            self._data.io.start_listening(user.id)

            text = None
            while text is None:
                text = self._data.io.pop_text(user.id)
                await asyncio.sleep(0.2)

            return text

        return await asyncio.get_event_loop().create_task(task())

    async def get_yes_no_answer(self,
                                user: SillyUser,
                                question: str | Dict[str | Sequence[str], str]) -> bool:
        option = await self.show_dialog(user, question,
                                        self._data.settings.labels.no,
                                        self._data.settings.labels.yes)
        return True if option else False

    # endregion

    # region Other

    async def start_broadcast(self, text: str | Dict[str | Sequence[str], str], user_ids: list[int] = None):
        async def _task(_text: str | Dict[str | Sequence[str], str], _user_ids: list[int] = None):
            all_users = self._data.users.get_all()
            users = all_users if user_ids is None else (user for user in all_users if user.id in user_ids)

            for user in users:
                await self.show_interruption(user, localize(_text, user.language_code))
                await asyncio.sleep(0.5)

        await asyncio.get_event_loop().create_task(_task(text, user_ids))

    # endregion

    # endregion

    # region Low-level messaging methods

    async def _edit_target_message(self, user: SillyUser, text: str, keyboard: InlineKeyboardMarkup):
        target_message_id = self._data.users.get_target_message_id(user.id)

        if target_message_id is None:
            await self._send_new_target_message(user, text, keyboard)
        else:
            try:
                await self._aiogram_bot.edit_message_text(chat_id=user.id, text=text,
                                                          message_id=target_message_id, reply_markup=keyboard)
            except Exception as e:
                await self._send_new_target_message(user, text, keyboard)

    async def _send_new_target_message(self, user: SillyUser, text: str,
                                       keyboard: InlineKeyboardMarkup, separate: bool = True):
        if separate:
            await self._send_separation_messages(user)

        message: AiogramMessage = await self._aiogram_bot.send_message(user.id, text, reply_markup=keyboard)
        self._data.users.set_target_message_id(user.id, message.message_id)

    async def _send_separation_messages(self, user: SillyUser):
        for i in range(0, 5):
            await self._aiogram_bot.send_message(user.id, text=self._data.settings.labels.emoji_separator)
            await asyncio.sleep(0.15)

    async def _replace_target_message(self, user: SillyUser, text: str, keyboard: InlineKeyboardMarkup):
        target_message_id = self._data.users.get_target_message_id(user.id)
        if target_message_id is not None:
            try:
                await self._aiogram_bot.delete_message(user.id, target_message_id)
            except Exception as e:
                ...

        await self._send_new_target_message(user, text, keyboard)

    async def _delete_target_message(self, user: SillyUser):
        target_message_id = self._data.users.get_target_message_id(user.id)
        if target_message_id is None:
            return

        try:
            await self._aiogram_bot.delete_message(user.id, target_message_id)
        except Exception as e:
            pass

    # endregion

    def __init__(self, aiogram_bot: AiogramBot, data: Data):
        self._aiogram_bot = aiogram_bot
        self._data = data

        self._logger = SillyLogger(PATH / "logs", self._data.settings.log_to_console)




    