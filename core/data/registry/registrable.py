from abc import abstractmethod
from typing import Optional, Tuple


class Registrable:

    @abstractmethod
    def establish_key(self, key: str, default_value: Optional[str] = None):
        raise NotImplementedError()

    @abstractmethod
    def remove_key(self, key: str):
        raise NotImplementedError()

    @abstractmethod
    def get_value(self, key: str | Tuple[str, int]):
        raise NotImplementedError()

    @abstractmethod
    def set_value(self,  key: str | Tuple[str, int], value: str):
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

