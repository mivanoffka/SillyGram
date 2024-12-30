class IO:
    _dialog_results: dict[int, int] = {}
    _users_text_inputs: dict[int, str] = {}
    _users_to_listen_for_input: list[int] = []
    _user_to_listen_for_dialog: list[int] = []

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

