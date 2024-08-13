import asyncio
from datetime import datetime
from utility import SillyDataSection


class Session(SillyDataSection):
    __statistics: dict[str, int] = {}
    __recent_users_id_list: list[int] = []
    __start_time: datetime = datetime.now()

    __dialog_results: dict[int, int] = {}
    __users_text_inputs: dict[int, str] = {}
    __users_to_listen: list[int] = []

    @property
    def recent_users_count(self) -> int:
        return len(self.__recent_users_id_list)

    @property
    def statistics(self) -> dict[str, int]:
        return self.__statistics

    def _increment_key(self, key: str, user_id: int):
        if key in self.__statistics:
            self.__statistics[key] += 1
        else:
            self.__statistics[key] = 1

        if user_id not in self.__recent_users_id_list and user_id is not None:
            self.__recent_users_id_list.append(user_id)

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

    def track(self, key: str):
        def decorator(function):
            async def wrapper(*args, **kwargs):
                user_id = None

                for arg in args:
                    if isinstance(arg, int):
                        user_id = arg
                        break

                self._increment_key(key, user_id)

                return await function(*args, **kwargs)

            return wrapper

        return decorator


