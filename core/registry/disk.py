from typing import Tuple

from .registrable import Registrable
from utility import SillyDbSection, SillyDB
from ..data.types import *


class DiskRegistry(Registrable, SillyDbSection):
    def _remove_key(self, key: str):
        with self._get_session() as session:
            registry_key = session.query(RegistryKey).filter_by(key=key).first()
            if registry_key:
                session.delete(registry_key)
                session.commit()

    def _is_user_value_not_default(self, key: str, user_id: int):
        with self._get_session() as session:
            registry_key = session.query(RegistryKey).filter_by(key=key[0]).first()
            if registry_key:
                registry_value = session.query(RegistryValue).filter_by(key_id=registry_key.id, user_id=user_id).first()
                if registry_value:
                    return registry_value.value is not None

        return False

    def _remove_key_entrances(self, key: str):
        with self._get_session() as session:
            registry_key = session.query(RegistryKey).filter_by(key=key[0]).first()
            if registry_key:
                registry_values = session.query(RegistryValue).filter_by(key_id=registry_key.id)
                for registry_value in registry_values:
                    session.delete(registry_value)
                session.commit()

    def _set_default(self, key: str, user: id):
        with self._get_session() as session:
            registry_value = session.query(RegistryValue).filter_by(key=key, user_id=user).first()
            if registry_value:
                session.delete(registry_value)
                session.commit()

    def _get_global_value(self, key: str) -> str:
        with self._get_session() as session:
            registry_key = session.query(RegistryKey).filter_by(key=key).first()
            if registry_key is None:
                raise KeyError(f"Key {key} not found")
            else:
                return registry_key.global_value

    def _get_local_value(self, key: Tuple[str, int]) -> str:
        with self._get_session() as session:
            registry_key = session.query(RegistryKey).filter_by(key=key[0]).first()
            if registry_key:
                return session.query(RegistryValue).filter_by(key_id=registry_key.id, user_id=key[1]).first().value
            else:
                raise KeyError(f"Key {key} not found")

    def _set_global_value(self, key: str, value: str):
        with self._get_session() as session:
            registry_key: RegistryKey = session.query(RegistryKey).filter_by(key=key).first()
            if registry_key:
                registry_key.global_value = value
            else:
                registry_key = RegistryKey(key=key, global_value=value)
                session.add(registry_key)
            session.commit()

    def _set_local_value(self, key: Tuple[str, int], value: str):
        with self._get_session() as session:
            key_id = session.query(RegistryKey).filter_by(key=key[0]).first().id
            registry_value: RegistryValue = session.query(RegistryValue).filter_by(key_id=key_id, user_id=key[1]).first()
            if registry_value:
                registry_value.value = value
            else:
                registry_value = RegistryValue(key_id=key_id, user_id=key[1], value=value)
                session.add(registry_value)
            session.commit()

    def _reset_keys(self):
        with self._get_session() as session:
            session.query(RegistryKey).delete()
            session.commit()

    def _reset_values(self):
        with self._get_session() as session:
            session.query(RegistryValue).delete()
            session.commit()

    def __init__(self, db: SillyDB) -> None:
        SillyDbSection.__init__(self, db)
        Registrable.__init__(self)
