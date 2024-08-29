from utility import SillyDbSection
from aiogram.types import User as AiogramUser
from core.data.types import User
from core.data.user import SillyUser
from datetime import datetime


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

    def get(self, user_id: int) -> SillyUser | None:
        with self._get_session() as session:
            return session.query(User).filter_by(id=user_id).first()

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


