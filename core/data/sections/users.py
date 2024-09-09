from typing import Optional

from utility import SillyDbSection
from aiogram.types import User as AiogramUser
from core.data.types import User, Admin, Ban
from core.data.user import SillyUser
from datetime import datetime, timedelta

from ...exceptions import SillyUserNotRegisteredError


class Users(SillyDbSection):

    def indicate(self, aiogram_user: AiogramUser) -> SillyUser:
        with self._get_session() as session:
            user = session.query(User).filter_by(id=aiogram_user.id).first()
            if not user:
                user = User(id=aiogram_user.id,
                            nickname=aiogram_user.username,
                            first_name=aiogram_user.first_name,
                            last_name=aiogram_user.last_name,
                            language_code=aiogram_user.language_code,
                            registered_at=datetime.now(),
                            last_seen_at=datetime.now())

                session.add(user)

            else:
                user.nickname = aiogram_user.username
                user.first_name = aiogram_user.first_name
                user.last_name = aiogram_user.last_name
                user.language_code = aiogram_user.language_code
                user.last_seen_at = datetime.now()

            session.commit()

            return SillyUser(id=user.id, nickname=user.nickname,
                             first_name=user.first_name, last_name=user.last_name, language_code=user.language_code,
                             registered_at=user.registered_at, last_seen_at=user.last_seen_at)

    def get(self, name_or_id: int | str) -> SillyUser | None:
        with self._get_session() as session:
            if isinstance(name_or_id, int):
                return session.query(User).filter_by(id=name_or_id).first()
            else:
                return session.query(User).filter_by(nickname=name_or_id).first()

    def get_all(self) -> tuple[SillyUser, ...]:
        with self._get_session() as session:
            return session.query(User)

    def get_target_message_id(self, user_id: int) -> int | None:
        with self._get_session() as session:
            return session.query(User).filter_by(id=user_id).first().target_message_id

    def set_target_message_id(self, user_id: int, message_id: int):
        with self._get_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            user.target_message_id = message_id
            session.commit()

    def get_current_page_name(self, user_id: int) -> str | None:
        with self._get_session() as session:
            return session.query(User).filter_by(id=user_id).first().current_page_name

    def set_current_page_name(self, user_id: int, page_name: str):
        with self._get_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            user.current_page_name = page_name
            session.commit()

    def is_admin(self, user_id: int) -> bool:
        with self._get_session() as session:
            return bool(session.query(Admin).filter_by(id=user_id).first())

    def promote(self, user_id: int):
        with self._get_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                raise SillyUserNotRegisteredError(f"User {user_id} is not registered")

            admin = session.query(Admin).filter_by(id=user_id).first()
            if not admin:
                admin = Admin(id=user_id)
                session.add(admin)
                session.commit()

    def demote(self, user_id: int):
        with self._get_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                raise SillyUserNotRegisteredError(f"User {user_id} is not registered")

            admin = session.query(Admin).filter_by(id=user_id).first()
            if admin:
                session.delete(admin)
                session.commit()

    def is_banned(self, user_id: int) -> bool:
        with self._get_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                raise SillyUserNotRegisteredError(f"User {user_id} is not registered")

            bans = session.query(Ban).filter_by(user_id=user_id).all()
            for ban in bans:
                if ban.expires > datetime.now() or ban.expires is None:
                    return True

            return False

    def get_ban_list(self):
        with self._get_session() as session:
            bans = session.query(Ban).filter_by(is_banned=True).all()
            bans_list = ((ban.user_id, ban.expires) for ban in bans)

            return bans_list

    def ban(self, user_id: int, expires: Optional[datetime] = None, lasts: Optional[timedelta] = None) -> datetime:
        if lasts and expires:
            raise ValueError()

        if lasts:
            expires = datetime.now() + lasts

        with self._get_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                raise SillyUserNotRegisteredError(f"User {user_id} is not registered")

            ban = Ban(user_id=user_id, starts=datetime.now(), expires=expires)
            session.add(ban)
            session.commit()

            return expires

        return None

    def unban(self, user_id: int):
        with self._get_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                raise SillyUserNotRegisteredError(f"User {user_id} is not registered")

            bans = session.query(Ban).filter(Ban.expires >= datetime.now()).all()
            for ban in bans:
                session.delete(ban)
            session.commit()

    def unban_all(self):
        with self._get_session() as session:
            session.query(Ban).delete()
            session.commit()



