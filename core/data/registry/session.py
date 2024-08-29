from typing import Optional, Dict, Tuple
from .registrable import Registrable


class SessionRegistry(Registrable):
    _keys: Dict[str, str]
    _registry: Dict[Tuple[str, int], str]

    def _set_local_value_for_all_users(self, key: str, value: str):
        for registry_key in self._registry.keys():
            if registry_key[0] == key:
                self._registry[registry_key] = value

    def _remove_key_globally(self, key: str):
        self._keys.pop(key)

    def _remove_key_locally(self, key: str):
        for registry_key in self._registry.keys():
            if registry_key[0] == key:
                self._registry.pop(registry_key)

    def _get_global_value(self, key: str) -> str:
        return self._keys[key]

    def _get_local_value(self, key: Tuple[str, int]) -> str:
        for registry_key in self._registry.keys():
            if registry_key[0] == key[0] and registry_key[1] == key[1]:
                return self._registry[registry_key]

        return self._keys[key[0]]

    def _set_global_value(self, key: str, value: str):
        self._keys[key] = value

    def _set_local_value(self, key: Tuple[str, int], value: str):
        self._registry[key] = value

    def __init__(self):
        super().__init__()
        self._registry = {}
        self._keys = {}
