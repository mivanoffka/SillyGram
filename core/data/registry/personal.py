from .registry import Registrable


class PersonalRegistry:
    _id: int
    _registry: Registrable

    def _key(self, subkey: str) -> tuple[str, int]:
        return subkey, self._id

    def set_value(self, key: str, value: str):
        self._registry.set_value(self._key(key), value)

    def get_value(self, key: str) -> str:
        return self._registry.get_value(self._key(key))

    def __getitem__(self, key: str) -> str:
        return self._registry.get_value(self._key(key))

    def __setitem__(self, key: str, value: str):
        self._registry.set_value(self._key(key), value)

    def __init__(self, user_id: int, registry: Registrable):
        self._id = user_id
        self._registry = registry

