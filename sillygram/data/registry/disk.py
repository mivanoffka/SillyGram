from typing import Optional, Any

from ..db import SillyDbSection, SillyDB
from ..orm import RegistryValueORM
from .registry import SillyRegistry


class SillyDiskRegistry(SillyRegistry, SillyDbSection):
    def __init__(self, db: SillyDB):
        SillyRegistry.__init__(self)
        SillyDbSection.__init__(self, db)

    def _exists(self, key_name: str, user_id: int | None) -> bool:
        with self._get_session() as session:
            existing = session.query(RegistryValueORM).filter_by(
                key_name=key_name, user_id=user_id
            )
            return existing is None

    def _add(self, key_name: str, user_id: int | None, value: Optional[str]):
        with self._get_session() as session:
            object = RegistryValueORM(key_name=key_name, user_id=user_id, value=value)
            session.add(object)
            session.commit()

    def _update(self, key_name: str, user_id: int | None, value: Optional[str]):
        with self._get_session() as session:
            object = session.query(RegistryValueORM).filter_by(
                key_name=key_name, user_id=user_id
            )
            if object is None:
                raise KeyError("")
            object.value = value
            session.commit()

    def _get(self, key_name: str, user_id: int | None):
        with self._get_session() as session:
            object = session.query(RegistryValueORM).filter_by(
                key_name=key_name, user_id=user_id
            )
            if object is None:
                raise KeyError("")
            return object.value