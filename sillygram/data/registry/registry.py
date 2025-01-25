from abc import abstractmethod, ABCMeta
from typing import Optional, Tuple


class SillyRegistry(metaclass=ABCMeta):
    class NotFound:
        _instance = None

        def __new__(cls):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

        def __eq__(self, other):
            return isinstance(other, SillyRegistry.NotFound)

    def set(self, key_name: str, user_id: Optional[int], value: Optional[str]):
        if self._exists(key_name, user_id):
            self._update(key_name, user_id, value)
        else:
            self._add(key_name, user_id, value)

    def get(self, key_name: str, user_id: Optional[int]) -> Optional[str] | 'SillyRegistry.NotFound':
        if self._exists(key_name, user_id):
            return self._get(key_name, user_id)
        else:
            return self.NotFound()

    @abstractmethod
    def _get(self, key_name: str, user_id) -> Optional[str]:
        raise NotImplementedError()

    @abstractmethod
    def _exists(self, key_name: str, user_id: Optional[int]) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def _update(self, key_name: str, user_id: Optional[int], value: Optional[str]):
        raise NotImplementedError()

    @abstractmethod
    def _add(self, key_name: str, user_id: Optional[int], value: Optional[str]):
        raise NotImplementedError()

    def __getitem__(self, key: Tuple[str, Optional[int]] | Tuple[Optional[int], str]) -> Optional[str] | 'SillyRegistry.NotFound':
        if isinstance(key, Tuple):
            if len(key) == 2:
                if (isinstance(key[0], int) or key[0] is None) and isinstance(
                    key[1], str
                ):
                    return self.get(key[1], key[0])
                elif (isinstance(key[1], int) or key[1] is None) and isinstance(
                    key[0], str
                ):
                    return self.get(key[0], key[1])

        raise TypeError("Invalid key format")

    def __setitem__(self, key: Tuple[str, Optional[int]] | Tuple[Optional[int], str], value: Optional[str]):
        if isinstance(key, Tuple):
            if len(key) == 2:
                if (isinstance(key[0], int) or key[0] is None) and isinstance(
                    key[1], str
                ):
                    return self.set(key[1], key[0], value)
                elif (isinstance(key[1], int) or key[1] is None) and isinstance(
                    key[0], str
                ):
                    return self.set(key[0], key[1], value)

        raise TypeError("Invalid key format")
