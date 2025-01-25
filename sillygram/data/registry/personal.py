from typing import Optional
from .registry import SillyRegistry


class SillyPersonalRegistry:
    _user_id: Optional[int]
    _registry: SillyRegistry

    def __init__(self, registry: SillyRegistry, user_id: Optional[int]):
        self._user_id = user_id
        self._registry = registry

    def set(self, key_name: str, value: Optional[str]):
        return self._registry.set(key_name, self._user_id, value)

    def get(self, key_name: str) -> Optional[str] | SillyRegistry.NotFound:
        return self._registry.get(key_name, self._user_id)

    def __getitem__(self, key: str) -> Optional[str] | SillyRegistry.NotFound:
        return self.get(key)

    def __setitem__(self, key: str, value: Optional[str]):
        return self.set(key, value)