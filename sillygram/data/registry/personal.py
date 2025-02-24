from typing import Optional

from ..orm import RegistryValueORM

from ..db import SillyDbSection, SillyDB
from .prototype import SillyRegistryPrototype
from collections.abc import MutableMapping
from .key import SillyRegistryKey


class SillyPersonalRegistry(SillyDbSection, MutableMapping):
    _user_id: int
    _registry: SillyRegistryPrototype

    def _global_key(self, name: str):
        return SillyRegistryKey(name=name, user_id=self._user_id)

    def __getitem__(self, key: str):
        return self._registry[self._global_key(key)]

    def __setitem__(self, key: str, value: str):
        value = str(value)
        self._registry[self._global_key(key)] = value

    def __delitem__(self, key):
        del self._registry[self._global_key(key)]

    def __iter__(self):
        with self._get_session() as session:
            objects = (
                session.query(RegistryValueORM).filter_by(user_id=self._user_id).all()
            )
            return iter(obj.key_name for obj in objects)

    def __len__(self):
        with self._get_session() as session:
            objects = (
                session.query(RegistryValueORM).filter(user_id=self._user_id).all()
            )
            return len(objects) if objects else 0

    def __init__(self, db: SillyDB, registry: SillyRegistryPrototype, user_id: int):
        SillyDbSection.__init__(self, registry._db)
        self._user_id = user_id
        self._registry = registry
