from abc import abstractmethod
from typing import Optional, Tuple


class Registrable:

    def establish_key(self, key: str, default_value: Optional[str] = None):
        self._set_global_value(key, default_value)
        self._remove_key_entrances(key)

    @abstractmethod
    def _set_default(self, key: str, user_id: int):
        raise NotImplementedError()

    @abstractmethod
    def _remove_key_entrances(self, key: str):
        raise NotImplementedError()

    def remove_key(self, key: str):
        self._remove_key_entrances(key)
        self._remove_key(key)

    def reset(self):
        self._reset_keys()
        self._reset_values()

    def reset_user(self, user_id: int):
        for key in self.get_keys():
            self._set_default(key, user_id)

    @abstractmethod
    def _reset_values(self):
        raise NotImplementedError()

    @abstractmethod
    def _reset_keys(self):
        raise NotImplementedError()

    def get_value(self, key: str | Tuple[str, int]):
        if isinstance(key, str):
            return self._get_global_value(key)
        elif isinstance(key, tuple) and isinstance(key[0], str) and isinstance(key[1], int) and len(key) == 2:
            if self._is_user_value_not_default(key[0], key[1]):
                return self._get_local_value(key)
            return self._get_global_value(key[0])
        else:
            raise KeyError("Invalid key format")

    @abstractmethod
    def _is_user_value_not_default(self, key: str, user_id: int):
        raise NotImplementedError()

    @abstractmethod
    def get_keys(self) -> tuple[str, ...]:
        raise NotImplementedError()

    def set_value(self,  key: str | Tuple[str, int], value: Optional[str]):
        if isinstance(key, str):
            self._set_global_value(key, value)
        elif isinstance(key, tuple) and isinstance(key[0], str) and isinstance(key[1], int) and len(key) == 2:
            if value:
                self._set_local_value(key, value)
            else:
                if self._is_user_value_not_default(key[0], key[1]):
                    self._set_default(key[0], key[1])
        else:
            raise KeyError("Invalid key format")

    @abstractmethod
    def _remove_key(self, key: str):
        raise NotImplementedError()

    @abstractmethod
    def _get_global_value(self, key: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _get_local_value(self, key: Tuple[str, int]) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _set_global_value(self, key: str, value: str):
        raise NotImplementedError()

    @abstractmethod
    def _set_local_value(self, key: Tuple[str, int], value: str):
        raise NotImplementedError()

    def __iadd__(self, other: str | Tuple[str, int]):
        if isinstance(other, str):
            self.establish_key(other)
        if isinstance(other, tuple) and len(other) == 2 and isinstance(other[0], str) and isinstance(other[1], str):
            self.establish_key(other[0], other[1])

    def __isub__(self, other: str):
        self.remove_key(other)

    def __getitem__(self, key: str | Tuple[str, int]):
        return self.get_value(key)

    def __setitem__(self, key: str | Tuple[str, int], value):
        self.set_value(key, value)

