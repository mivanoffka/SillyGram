from collections.abc import MutableMapping
from typing import Optional, Tuple, Sequence, Any

from ..db import SillyDbSection, SillyDB
from ..orm import RegistryValueORM
from .key import SillyRegistryKey


class SillyRegistryPrototype(MutableMapping, SillyDbSection):
    def __init__(self, db: SillyDB):
        SillyDbSection.__init__(self, db)

    def __getitem__(self, key: SillyRegistryKey):
        with self._get_session() as session:
            object = (
                session.query(RegistryValueORM)
                .filter_by(key_name=key.name, user_id=key.user_id)
                .first()
            )
            if object:
                return object.value
            raise KeyError("")

    def __setitem__(self, key: SillyRegistryKey, value: str):
        value = str(value)

        with self._get_session() as session:
            object = (
                session.query(RegistryValueORM)
                .filter_by(key_name=key.name, user_id=key.user_id)
                .first()
            )
            if object is None:
                object = RegistryValueORM(
                    key_name=key.name, user_id=key.user_id, value=value
                )
                session.add(object)
            else:
                object.value = value

            session.commit()

    def __delitem__(self, key: SillyRegistryKey):
        with self._get_session() as session:
            object = (
                session.query(RegistryValueORM)
                .filter_by(key_name=key.name, user_id=key.user_id)
                .first()
            )
            if object is None:
                raise KeyError("")
            session.delete(object)
            session.commit()

    def __iter__(self):
        with self._get_session() as session:
            objects = session.query(RegistryValueORM).all()
            return iter(
                SillyRegistryKey(name=obj.key_name, user_id=obj.user_id)
                for obj in objects
            )

    def __len__(self):
        with self._get_session() as session:
            objects = session.query(RegistryValueORM).all()
            return len(objects) if objects else 0
