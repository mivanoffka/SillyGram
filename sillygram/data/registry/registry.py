from abc import abstractmethod, ABCMeta
from typing import Optional, Tuple

class SillyRegistry(metaclass=ABCMeta):
    def set(self, key_name: str, user_id: Optional[int], value: str):
        if self._exists(key_name, user_id):
            self._update(key_name, user_id, value)
        else:
            self._add(key_name, user_id, value)

    def get(self, key_name: str, user_id: Optional[int]) -> Optional[str]:
        if self._exists(key_name, user_id):
            return self._get(key_name, user_id)
        else:
            return None

    def delete(self, key_name: str, user_id: Optional[int]):
        if self._exists(key_name, user_id):
            self._delete(key_name, user_id)

    @abstractmethod
    def _get(self, key_name: str, user_id) -> Optional[str]:
        raise NotImplementedError()

    @abstractmethod
    def _exists(self, key_name: str, user_id: Optional[int]) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def _update(self, key_name: str, user_id: Optional[int], value: str):
        raise NotImplementedError()

    @abstractmethod
    def _add(self, key_name: str, user_id: Optional[int], value: str):
        raise NotImplementedError()

    @abstractmethod
    def _delete(self, key_name: str, user_id: Optional[int]):
        raise NotImplementedError()

    def __getitem__(self, key: Tuple[str, Optional[int]] | Tuple[Optional[int], str]) -> Optional[str]:
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

    def __setitem__(self, key: Tuple[str, Optional[int]] | Tuple[Optional[int], str], value: str):
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
