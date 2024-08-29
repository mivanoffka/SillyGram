from abc import abstractmethod
from typing import Optional, Tuple


class Registrable:

    def establish_key(self, key: str, default_value: Optional[str] = None):
        self._set_global_value(key, default_value)
        self._set_local_value_for_all_users(key, default_value)

    def remove_key(self, key: str):
        self._remove_key_globally(key)
        self._remove_key_locally(key)

    def get_value(self, key: str | Tuple[str, int]):
        if isinstance(key, str):
            return self._get_global_value(key)
        elif isinstance(key, tuple) and isinstance(key[0], str) and isinstance(key[1], int) and len(key) == 2:
            return self._get_local_value(key)
        else:
            raise KeyError("Invalid key format")

    def set_value(self,  key: str | Tuple[str, int], value: str):
        if isinstance(key, str):
            self._set_global_value(key, value)

        elif isinstance(key, tuple) and isinstance(key[0], str) and isinstance(key[1], int) and len(key) == 2:
            self._set_local_value(key, value)
        else:
            raise KeyError("Invalid key format")

    @abstractmethod
    def _remove_key_globally(self, key: str):
        raise NotImplementedError()

    @abstractmethod
    def _remove_key_locally(self, key: str):
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

    @abstractmethod
    def _set_local_value_for_all_users(self, key: str, value: str):
        raise NotImplementedError()

    def __iadd__(self, other: str | Tuple[str, str]):
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

