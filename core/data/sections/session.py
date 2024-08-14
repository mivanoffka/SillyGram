from datetime import datetime
from utility import SillyDataSection


class Session(SillyDataSection):
    __start_time: datetime = datetime.now()

    __dialog_results: dict[int, int] = {}
    __users_text_inputs: dict[int, str] = {}
    __users_to_listen: list[int] = []

    def push_text(self, user_id: int, text: str):
        if user_id not in self.__users_to_listen:
            return
        self.__users_text_inputs[user_id] = text

    def pop_text(self, user_id: int) -> str | None:
        if user_id not in self.__users_text_inputs.keys():
            return None
        return self.__users_text_inputs.pop(user_id)

    def push_dialog_result(self, user_id: int, dialog_result: int):
        self.__dialog_results[user_id] = dialog_result

    def pop_dialog_result(self, user_id: int) -> int | None:
        if user_id not in self.__dialog_results.keys():
            return None
        return self.__dialog_results.pop(user_id)

    def start_listening(self, user_id: int):
        if user_id not in self.__users_to_listen:
            self.__users_to_listen.append(user_id)

    def stop_listening(self, user_id: int):
        if user_id in self.__users_to_listen:
            self.__users_to_listen.remove(user_id)



