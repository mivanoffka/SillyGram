from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...manager import SillyManager

import asyncio
from typing import Dict, List


class IO:
    _manager: SillyManager

    _dialog_results: Dict[int, int] = {}
    _users_text_inputs: Dict[int, str] = {}
    _users_to_listen_for_input: List[int] = []
    _user_to_listen_for_dialog: List[int] = []

    _refreshing_count_downs: Dict[int, int] = {}
    _to_delete: List[int] = []
    _to_add: List[int] = []

    def push_to_add(self, user_id: int):
        if user_id not in self._to_add:
            self._to_add.append(user_id)

    def push_to_delete(self, user_id: int):
        if user_id not in self._to_delete:
            self._to_delete.append(user_id)

    def push_text(self, user_id: int, text: str):
        if user_id not in self._users_to_listen_for_input:
            return
        self._users_text_inputs[user_id] = text

    def pop_text(self, user_id: int) -> str | None:
        if user_id not in self._users_text_inputs.keys():
            return None
        return self._users_text_inputs.pop(user_id)

    def push_dialog_result(self, user_id: int, dialog_result: int):
        if user_id not in self._user_to_listen_for_dialog:
            return
        self._dialog_results[user_id] = dialog_result

    def pop_dialog_result(self, user_id: int) -> int | None:
        if user_id not in self._dialog_results.keys():
            return None
        return self._dialog_results.pop(user_id)

    def is_input_listening(self, user_id: int):
        return user_id in self._users_to_listen_for_input

    def start_input_listening(self, user_id: int):
        if user_id not in self._users_to_listen_for_input:
            self._users_to_listen_for_input.append(user_id)

    def stop_input_listening(self, user_id: int):
        if user_id in self._users_to_listen_for_input:
            self._users_to_listen_for_input.remove(user_id)

    def start_dialog_listening(self, user_id: int):
        if user_id not in self._user_to_listen_for_dialog:
            self._user_to_listen_for_dialog.append(user_id)

    def stop_dialog_listening(self, user_id: int):
        if user_id in self._user_to_listen_for_dialog:
            self._user_to_listen_for_dialog.remove(user_id)

    def is_dialog_listening(self, user_id: int):
        return user_id in self._user_to_listen_for_dialog

    async def _refreshing_countdowns_loop(self):
        while True:
            await asyncio.sleep(0.1)
            for user_id in self._to_delete:
                if user_id in self._refreshing_count_downs:
                    self._refreshing_count_downs.pop(user_id)

            for user_id in self._to_add:
                self._refreshing_count_downs[user_id] = 5

            self._to_delete.clear()
            self._to_add.clear()

            for user_id in self._refreshing_count_downs:
                if self._refreshing_count_downs[user_id] >= 0:
                    self._refreshing_count_downs[user_id] -= 1

                if self._refreshing_count_downs[user_id] == -1:
                    user = self._manager.users.get(user_id)
                    if user:
                        await self._manager.refresh_page(user)

    def start_loop(self):
        asyncio.create_task(self._refreshing_countdowns_loop())


    def __init__(self, manager: SillyManager):
        self._manager = manager
