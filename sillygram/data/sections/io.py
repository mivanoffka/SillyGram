class IO:
    _dialog_results: dict[int, int] = {}
    _users_text_inputs: dict[int, str] = {}
    _users_to_listen: list[int] = []

    def push_text(self, user_id: int, text: str):
        if user_id not in self._users_to_listen:
            return
        self._users_text_inputs[user_id] = text

    def pop_text(self, user_id: int) -> str | None:
        if user_id not in self._users_text_inputs.keys():
            return None
        return self._users_text_inputs.pop(user_id)

    def push_dialog_result(self, user_id: int, dialog_result: int):
        self._dialog_results[user_id] = dialog_result

    def pop_dialog_result(self, user_id: int) -> int | None:
        if user_id not in self._dialog_results.keys():
            return None
        return self._dialog_results.pop(user_id)

    def is_listening(self, user_id: int):
        return user_id in self._users_to_listen

    def start_listening(self, user_id: int):
        if user_id not in self._users_to_listen:
            self._users_to_listen.append(user_id)

    def stop_listening(self, user_id: int):
        if user_id in self._users_to_listen:
            self._users_to_listen.remove(user_id)



