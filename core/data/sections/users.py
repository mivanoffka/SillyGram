from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Tuple, Optional, List, Dict

from utility import SillyDbSection, SillyDB
from ..types import User, Admin, Ban

if TYPE_CHECKING:
    from core.management.manager import SillyManager
    
from ..user import SillyUser


class Users(SillyDbSection):
    _users_data: Users
    _manager: SillyManager

    def __init__(self, db: SillyDB, manager: SillyManager):
        super().__init__(db)
        self._manager = manager

    # region System

    def _create_silly_user(self, user_id: int):
        return SillyUser(user_id=user_id, manager=self._manager)

    def _validate(self, nickname_or_id: int | str) -> int:
        with self._get_session() as session:
            id_to_return: Optional[int] = None
            if isinstance(nickname_or_id, int):
                id_to_return = session.query(User).filter_by(id=nickname_or_id).first().id
            elif isinstance(nickname_or_id, str):
                id_to_return = session.query(User).filter_by(nickname=nickname_or_id).first().id
            else:
                raise TypeError()

            if not id_to_return:
                raise KeyError()

            return id_to_return

    # endregion

    # region Attributes

    def get_nick_name(self, nickname_or_id: int | str) -> str:
        with self._get_session() as session:
            return session.query(User).filter_by(id=self._validate(nickname_or_id)).first().nickname

    def get_first_name(self, nickname_or_id: int | str) -> str:
        with self._get_session() as session:
            return session.query(User).filter_by(id=self._validate(nickname_or_id)).first().first_name

    def get_last_name(self, nickname_or_id: int | str) -> str:
        with self._get_session() as session:
            return session.query(User).filter_by(id=self._validate(nickname_or_id)).first().last_name

    def get_registration_date(self, nickname_or_id: int | str) -> datetime:
        with self._get_session() as session:
            return session.query(User).filter_by(id=self._validate(nickname_or_id)).first().registered_at

    def get_last_visit_date(self, nickname_or_id: int | str) -> datetime:
        with self._get_session() as session:
            return session.query(User).filter_by(id=self._validate(nickname_or_id)).first().last_visited

    def get_language_code(self, nickname_or_id: int | str) -> str:
        with self._get_session() as session:
            return session.query(User).filter_by(id=self._validate(nickname_or_id)).first().language_code

    def is_banned(self, nickname_or_id: int | str) -> bool:
        with self._get_session() as session:
            return bool(session.query(Ban).filter_by(id=self._validate(nickname_or_id)).all())

    def is_admin(self, nickname_or_id: int | str) -> bool:
        with self._get_session() as session:
            return bool(session.query(Admin).filter_by(id=self._validate(nickname_or_id)).all())

    def get_ban_expiration_date(self, nickname_or_id: int | str) -> Optional[datetime]:
        with self._get_session() as session:
            ban = session.query(Ban).filter_by(id=self._validate(nickname_or_id)).first()
            return ban.expires if ban else None

    # endregion

    # region Common

    def get(self, nickname_or_id: int | str) -> SillyUser:
        return self._create_silly_user(self._validate(nickname_or_id))

    def get_all(self) -> tuple[SillyUser, ...]:
        with self._get_session() as session:
            return tuple(self._create_silly_user(user.id) for user in session.query(User).all())

    # endregion

    # region Admins

    def get_all_admins(self) -> tuple[SillyUser, ...]:
        with self._get_session() as session:
            return tuple(self._create_silly_user(user.id) for user in session.query(Admin).all())

    def promote(self, nickname_or_id: int | str):
        user_id = self._validate(nickname_or_id)
        with self._get_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            admin = session.query(Admin).filter_by(id=user_id).first()
            if not admin:
                admin = Admin(id=user_id)
                session.add(admin)
                session.commit()

    def demote(self, nickname_or_id: int | str):
        user_id = self._validate(nickname_or_id)
        with self._get_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            admin = session.query(Admin).filter_by(id=user_id).first()
            if admin:
                session.delete(admin)
                session.commit()

    # endregion

    # region Banned

    def get_all_banned(self) -> tuple[SillyUser, ...]:
        with self._get_session() as session:
            return tuple(self._create_silly_user(user.id) for user in session.query(Ban).all())

    def ban(self, nickname_or_id: int | str, duration: timedelta):
        user_id = self._validate(nickname_or_id)
        expires = datetime.now() + duration

        with self._get_session() as session:
            ban = Ban(user_id=user_id, starts=datetime.now(), expires=expires)
            session.add(ban)
            session.commit()

            return expires

    def unban(self, nickname_or_id: int | str):
        user_id = self._validate(nickname_or_id)

        with self._get_session() as session:
            ban = session.query(Ban).filter_by(user_id=user_id).first()
            if ban:
                session.delete(ban)
                session.commit()

    def unban_all(self):
        with self._get_session() as session:
            session.query(Ban).delete()
            session.commit()

    # endregion
