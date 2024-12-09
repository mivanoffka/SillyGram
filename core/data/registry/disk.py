from typing import Tuple

from .registrable import Registrable
from utility import SillyDbSection, SillyDB
from core.data.orm import RegistryKeyORM, RegistryValueORM


class DiskRegistry(Registrable, SillyDbSection):
    def _remove_key(self, key: str):
        with self._get_session() as session:
            registry_key = session.query(RegistryKeyORM).filter_by(key=key).first()
            if registry_key:
                session.delete(registry_key)
                session.commit()

    def _is_user_value_not_default(self, key: str, user_id: int):
        with self._get_session() as session:
            registry_key = session.query(RegistryKeyORM).filter_by(key=key[0]).first()
            if registry_key:
                registry_value = session.query(RegistryValueORM).filter_by(key_id=registry_key.id, user_id=user_id).first()
                if registry_value:
                    return registry_value.value is not None

        return False

    def _remove_key_entrances(self, key: str):
        with self._get_session() as session:
            registry_key = session.query(RegistryKeyORM).filter_by(key=key[0]).first()
            if registry_key:
                registry_values = session.query(RegistryValueORM).filter_by(key_id=registry_key.id)
                for registry_value in registry_values:
                    session.delete(registry_value)
                session.commit()

    def _set_default(self, key: str, user_id: int):
        with self._get_session() as session:
            registry_key = session.query(RegistryKeyORM).filter_by(key=key).first()
            if not registry_key:
                return
            registry_value = session.query(RegistryValueORM).filter_by(key_id=registry_key.id, user_id=user_id).first()
            if registry_value:
                session.delete(registry_value)
                session.commit()

    def _get_global_value(self, key: str) -> str:
        with self._get_session() as session:
            registry_key = session.query(RegistryKeyORM).filter_by(key=key).first()
            if registry_key is None:
                raise KeyError(f"Key {key} not found")
            else:
                return registry_key.global_value

    def _get_local_value(self, key: Tuple[str, int]) -> str:
        with self._get_session() as session:
            registry_key = session.query(RegistryKeyORM).filter_by(key=key[0]).first()
            if registry_key:
                return session.query(RegistryValueORM).filter_by(key_id=registry_key.id, user_id=key[1]).first().value
            else:
                raise KeyError(f"Key {key} not found")

    def _set_global_value(self, key: str, value: str):
        with self._get_session() as session:
            registry_key: RegistryKeyORM = session.query(RegistryKeyORM).filter_by(key=key).first()
            if registry_key:
                registry_key.global_value = value
            else:
                registry_key = RegistryKeyORM(key=key, global_value=value)
                session.add(registry_key)
            session.commit()

    def _set_local_value(self, key: Tuple[str, int], value: str):
        with self._get_session() as session:
            key_id = session.query(RegistryKeyORM).filter_by(key=key[0]).first().id
            registry_value: RegistryValueORM = session.query(RegistryValueORM).filter_by(key_id=key_id, user_id=key[1]).first()
            if registry_value:
                registry_value.value = value
            else:
                registry_value = RegistryValueORM(key_id=key_id, user_id=key[1], value=value)
                session.add(registry_value)
            session.commit()

    def _reset_keys(self):
        with self._get_session() as session:
            session.query(RegistryKeyORM).delete()
            session.commit()

    def _reset_values(self):
        with self._get_session() as session:
            session.query(RegistryValueORM).delete()
            session.commit()

    def get_keys(self) -> tuple[str, ...]:
        with self._get_session() as session:
            registry_keys = session.query(RegistryKeyORM).all()
            return tuple(registry_key.key for registry_key in registry_keys)

    def __init__(self, db: SillyDB) -> None:
        SillyDbSection.__init__(self, db)
        Registrable.__init__(self)
