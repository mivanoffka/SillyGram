from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Optional

from utility import SillyDbSection, SillyDB
from ..orm import UserORM, AdminORM, BanORM

if TYPE_CHECKING:
    from ...manager import SillyManager
    
from ...user import SillyUser


class Users(SillyDbSection):
    _manager: SillyManager

    def __init__(self, db: SillyDB, manager: SillyManager):
        super().__init__(db)
        self._manager = manager

    # region System

    def _create_silly_user(self, user_id: int):
        with self._get_session() as session:
            user = session.query(UserORM).filter_by(id=user_id).first()
            if not user:
                raise KeyError()
            return SillyUser(user_id=user_id, manager=self._manager)

    def _validate(self, nickname_or_id: int | str) -> int:
        with self._get_session() as session:
            id_to_return: Optional[int] = None
            if isinstance(nickname_or_id, int):
                id_to_return = session.query(UserORM).filter_by(id=nickname_or_id).first().id 
            elif isinstance(nickname_or_id, str):
                id_to_return = session.query(UserORM).filter_by(nickname=nickname_or_id).first().id
            else:
                raise TypeError()

            if not id_to_return:
                raise KeyError()

            return id_to_return

    # endregion

    # region Attributes

    def get_nick_name(self, nickname_or_id: int | str) -> str:
        with self._get_session() as session:
            return session.query(UserORM).filter_by(id=self._validate(nickname_or_id)).first().nickname

    def get_first_name(self, nickname_or_id: int | str) -> str:
        with self._get_session() as session:
            return session.query(UserORM).filter_by(id=self._validate(nickname_or_id)).first().first_name

    def get_last_name(self, nickname_or_id: int | str) -> str:
        with self._get_session() as session:
            return session.query(UserORM).filter_by(id=self._validate(nickname_or_id)).first().last_name

    def get_registration_date(self, nickname_or_id: int | str) -> datetime:
        with self._get_session() as session:
            return session.query(UserORM).filter_by(id=self._validate(nickname_or_id)).first().registered_at

    def get_last_visit_date(self, nickname_or_id: int | str) -> datetime:
        with self._get_session() as session:
            return session.query(UserORM).filter_by(id=self._validate(nickname_or_id)).first().last_visited

    def get_language_code(self, nickname_or_id: int | str) -> str:
        with self._get_session() as session:
            return session.query(UserORM).filter_by(id=self._validate(nickname_or_id)).first().language_code

    def is_banned(self, nickname_or_id: int | str) -> bool:
        with self._get_session() as session:
            return bool(session.query(BanORM).filter_by(id=self._validate(nickname_or_id)).all())

    def is_admin(self, nickname_or_id: int | str) -> bool:
        with self._get_session() as session:
            return bool(session.query(AdminORM).filter_by(id=self._validate(nickname_or_id)).all())

    def get_ban_expiration_date(self, nickname_or_id: int | str) -> Optional[datetime]:
        with self._get_session() as session:
            ban = session.query(BanORM).filter_by(id=self._validate(nickname_or_id)).first()
            return ban.expires if ban else None

    # endregion

    # region Common

    def get(self, nickname_or_id: int | str) -> Optional[SillyUser]:
        try:
            return self._create_silly_user(self._validate(nickname_or_id))
        except Exception:
            return None

    def get_all(self) -> tuple[SillyUser, ...]:
        with self._get_session() as session:
            return tuple(self._create_silly_user(user.id) for user in session.query(UserORM).all())

    # endregion

    # region Admins

    def get_all_admins(self) -> tuple[SillyUser, ...]:
        with self._get_session() as session:
            return tuple(self._create_silly_user(user.id) for user in session.query(AdminORM).all())

    def promote(self, nickname_or_id: int | str):
        user_id = self._validate(nickname_or_id)
        with self._get_session() as session:
            admin = session.query(AdminORM).filter_by(id=user_id).first()
            if not admin:
                admin = AdminORM(id=user_id)
                session.add(admin)
                session.commit()

    def demote(self, nickname_or_id: int | str):
        user_id = self._validate(nickname_or_id)
        with self._get_session() as session:
            admin = session.query(AdminORM).filter_by(id=user_id).first()
            if admin:
                session.delete(admin)
                session.commit()

    # endregion

    # region Banned

    def get_all_banned(self) -> tuple[SillyUser, ...]:
        with self._get_session() as session:
            return tuple(self._create_silly_user(user.id) for user in session.query(BanORM).all())

    def ban(self, nickname_or_id: int | str, duration: timedelta):
        user_id = self._validate(nickname_or_id)
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
        user_id = self._validate(nickname_or_id)

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
