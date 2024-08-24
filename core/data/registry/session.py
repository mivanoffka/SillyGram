from typing import Optional, Dict, List, Tuple, Callable
from .registrable import Registrable


class SessionRegistry(Registrable):
    _keys: Dict[str, str]
    _registry: Dict[Tuple[str, int], str]

    def establish_key(self, key: str, default_value: Optional[str] = None):
        self._keys[key] = default_value

    def remove_key(self, key: str):
        self._keys.pop(key)

    def get_value(self, key: str | Tuple[str, int]):
        if isinstance(key, str):
            return self._get_global_value(key)
        elif isinstance(key, tuple) and isinstance(key[0], str) and isinstance(key[1], int) and len(key) == 2:
            return self._get_local_value(key)
        else:
            raise KeyError("Invalid key format")

    def _get_global_value(self, key: str) -> str:
        return self._keys[key]

    def _get_local_value(self, key: Tuple[str, int]) -> str:
        for registry_key in self._registry.keys():
            if registry_key[0] == key[0] and registry_key[1] == key[1]:
                return self._registry[registry_key]

        return self._keys[key[0]]

    def set_value(self,  key: str | Tuple[str, int], value: str):
        if isinstance(key, str):
            if key in self._keys:
                self._keys[key] = value
            else:
                raise KeyError("Key {} is not present in the session registry".format(key))

        elif isinstance(key, tuple) and isinstance(key[0], str) and isinstance(key[1], int) and len(key) == 2:
            if key[0] not in self._keys:
                raise KeyError("Key {} is not present in the session registry".format(key))

            self._registry[key] = value
        else:
            raise KeyError("Invalid key format")

    def __init__(self):
        super().__init__()
        self._registry = {}
        self._keys = {}
