from typing import Optional, Dict, Tuple
from .registrable import Registrable


class SessionRegistry(Registrable):

    _keys: Dict[str, str]
    _registry: Dict[Tuple[str, int], str]

    def _remove_key_entrances(self, key: str):
        to_pop = []

        for registry_key in self._registry.keys():
            if registry_key[0] == key:
                to_pop.append(registry_key)

        for registry_key in to_pop:
            self._registry.pop(registry_key)

    def _set_default(self, key: str, user: int):
        self._registry.pop((key, user))

    def _remove_key(self, key: str):
        self._keys.pop(key)

    def _get_global_value(self, key: str) -> str:
        return self._keys[key]

    def _get_local_value(self, key: Tuple[str, int]):
        return self._registry[key]

    def _is_user_value_not_default(self, key: str, user_id: int):
        return (key, user_id) in self._registry.keys()

    def _set_global_value(self, key: str, value: str):
        self._keys[key] = value

    def _set_local_value(self, key: Tuple[str, int], value: str):
        self._registry[key] = value

    def __init__(self):
        super().__init__()
        self._registry = {}
        self._keys = {}



