from typing import Optional, Any

from ..db import SillyDbSection, SillyDB
from ..orm import RegistryValueORM
from .registry import SillyRegistry


class SillyDiskRegistry(SillyRegistry, SillyDbSection):
    def __init__(self, db: SillyDB):
        SillyRegistry.__init__(self)
        SillyDbSection.__init__(self, db)

    def _validate_user_id(self, user_id: int | None) -> int:
        return user_id if user_id is not None else 0

    def _exists(self, key_name: str, user_id: int | None) -> bool:
        user_id = self._validate_user_id(user_id)

        with self._get_session() as session:
            existing = session.query(RegistryValueORM).filter_by(
                key_name=key_name, user_id=user_id
            ).first()
            return bool(existing)

    def _add(self, key_name: str, user_id: int | None, value: str):
        user_id = self._validate_user_id(user_id)

        with self._get_session() as session:
            object = RegistryValueORM(key_name=key_name, user_id=user_id, value=value)
            session.add(object)
            session.commit()

    def _update(self, key_name: str, user_id: int | None, value: str):
        user_id = self._validate_user_id(user_id)

        with self._get_session() as session:
            object = session.query(RegistryValueORM).filter_by(
                key_name=key_name, user_id=user_id
            ).first()
            if object is None:
                raise KeyError("")
            object.value = value

            session.commit()

    def _get(self, key_name: str, user_id: int | None):
        user_id = self._validate_user_id(user_id)

        with self._get_session() as session:
            object = (
                session.query(RegistryValueORM)
                .filter_by(key_name=key_name, user_id=user_id)
                .first()
            )
            if object is None:
                raise KeyError("")
            return object.value

    def _delete(self, key_name: str, user_id: int | None):
        user_id = self._validate_user_id(user_id)

        with self._get_session() as session:
            object = session.query(RegistryValueORM).filter_by(
                key_name=key_name, user_id=user_id
            ).first()
            if object is None:
                raise KeyError("")
            session.delete(object)
            session.commit()
