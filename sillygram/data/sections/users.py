from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Optional

from ..registry import SillyRegistry
from ..db import SillyDbSection, SillyDB
from ..orm import PrivilegeORM, UserORM, BanORM

if TYPE_CHECKING:
    from ...manager import SillyManager

from ...user import SillyUser


class Users(SillyDbSection):
    _manager: SillyManager
    _registry: SillyRegistry

    def __init__(self, db: SillyDB, manager: SillyManager, registry: SillyRegistry):
        super().__init__(db)
        self._manager = manager
        self._registry = registry

    # region System

    def _get_or_create_entity(self, user_id: int):
        with self._get_session() as session:
            user = session.query(UserORM).filter_by(id=user_id).first()
            if not user:
                raise KeyError()
            return SillyUser(
                user_id=user_id, manager=self._manager, registry=self._registry
            )

    def _validate_and_get_id(self, nickname_or_id: int | str) -> int:
        with self._get_session() as session:

            kwargs = (
                {"nickname": nickname_or_id}
                if isinstance(nickname_or_id, str)
                else {"id": nickname_or_id}
            )

            user = session.query(UserORM).filter_by(**kwargs).first()

            if not user:
                raise KeyError()

            return user.id

    # endregion

    # region Attributes

    def get_nick_name(self, nickname_or_id: int | str) -> str | None:
        with self._get_session() as session:
            user = (
                session.query(UserORM)
                .filter_by(id=self._validate_and_get_id(nickname_or_id))
                .first()
            )

            return user.nickname if user else None

    def get_first_name(self, nickname_or_id: int | str) -> Optional[str]:
        with self._get_session() as session:
            user = (
                session.query(UserORM)
                .filter_by(id=self._validate_and_get_id(nickname_or_id))
                .first()
            )
            return user.first_name if user else None

    def get_last_name(self, nickname_or_id: int | str) -> Optional[str]:
        with self._get_session() as session:
            user = (
                session.query(UserORM)
                .filter_by(id=self._validate_and_get_id(nickname_or_id))
                .first()
            )
            return user.last_name if user else None

    def get_registration_date(self, nickname_or_id: int | str) -> Optional[datetime]:
        with self._get_session() as session:
            user = (
                session.query(UserORM)
                .filter_by(id=self._validate_and_get_id(nickname_or_id))
                .first()
            )
            return user.registered_at if user else None

    def get_last_visit_date(self, nickname_or_id: int | str) -> Optional[datetime]:
        with self._get_session() as session:
            user = (
                session.query(UserORM)
                .filter_by(id=self._validate_and_get_id(nickname_or_id))
                .first()
            )

            return user.last_seen_at if user else None

    def get_language_code(self, nickname_or_id: int | str) -> Optional[str]:
        with self._get_session() as session:
            user = (
                session.query(UserORM)
                .filter_by(id=self._validate_and_get_id(nickname_or_id))
                .first()
            )
            return user.language_code if user else None

    def is_banned(self, nickname_or_id: int | str) -> bool:
        with self._get_session() as session:
            return bool(
                session.query(BanORM)
                .filter_by(id=self._validate_and_get_id(nickname_or_id))
                .all()
            )

    def get_ban_expiration_date(self, nickname_or_id: int | str) -> Optional[datetime]:
        with self._get_session() as session:
            ban = (
                session.query(BanORM)
                .filter_by(id=self._validate_and_get_id(nickname_or_id))
                .first()
            )
            return ban.expires if ban else None

    # endregion

    # region Common

    def get(self, nickname_or_id: int | str) -> SillyUser:
        return self._get_or_create_entity(self._validate_and_get_id(nickname_or_id))

    def get_all(self) -> tuple[SillyUser, ...]:
        with self._get_session() as session:
            return tuple(
                self._get_or_create_entity(user.id)
                for user in session.query(UserORM).all()
            )

    # endregion

    # region PRIVILEGEs

    def get_privilege_name(self, nickname_or_id: int | str) -> Optional[str]:
        with self._get_session() as session:
            user = (
                session.query(UserORM)
                .filter_by(id=self._validate_and_get_id(nickname_or_id))
                .first()
            )

            if user is None:
                return None

            privilege = user.privilege

            if privilege:
                return privilege.name
            else:
                return None

    def set_privilege(
        self, nickname_or_id: int | str, privilege_name: Optional[str] = None
    ):
        user_id = self._validate_and_get_id(nickname_or_id)
        with self._get_session() as session:
            user = session.query(UserORM).filter_by(id=user_id).first()

            if user is None:
                return

            if privilege_name is None:
                user.privilege_id = None
                return
            privilege = (
                session.query(PrivilegeORM).filter_by(name=privilege_name).first()
            )

            if privilege is None:
                return

            user.privilege_id = privilege.id
            session.commit()

    # endregion

    # region Banned

    def get_all_banned(self) -> tuple[SillyUser, ...]:
        with self._get_session() as session:
            return tuple(
                self._get_or_create_entity(user.id)
                for user in session.query(BanORM).all()
            )

    def ban(self, nickname_or_id: int | str, duration: timedelta):
        user_id = self._validate_and_get_id(nickname_or_id)
        expires = datetime.now() + duration

        with self._get_session() as session:
            ban = session.query(BanORM).filter_by(id=user_id).first()

            if not ban:
                ban = BanORM(id=user_id, expires=expires)
                session.add(ban)
            elif expires > ban.expires:
                ban.expires = expires
            session.commit()

            return expires

    def unban(self, nickname_or_id: int | str):
        user_id = self._validate_and_get_id(nickname_or_id)

        with self._get_session() as session:
            ban = session.query(BanORM).filter_by(id=user_id).first()
            if ban:
                session.delete(ban)
                session.commit()

    def unban_all(self):
        with self._get_session() as session:
            session.query(BanORM).delete()
            session.commit()

    # endregion
