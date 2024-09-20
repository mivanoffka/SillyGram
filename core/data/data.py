from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import desc

if TYPE_CHECKING:
    from core.manager import SillyManager

from datetime import datetime, timedelta

from utility import SillyDB
from .sections import IO, Pages, Users
from .orm import DECLARATIVE_BASE, UserORM, RecentUserORM, StatisticsUnitORM
from ..ui import SillyPage
from .settings_and_defaults import SillySettings
from core.data.registry import SillyRegistry

from aiogram.types import User as AiogramUser


class Data(SillyDB):
    _io: IO
    _pages: Pages
    _settings: SillySettings
    _registry: SillyRegistry
    _users: Users

    @property
    def users(self) -> Users:
        return self._users

    @property
    def io(self) -> IO:
        return self._io

    @property
    def pages(self) -> Pages:
        return self._pages

    @property
    def settings(self) -> SillySettings:
        return self._settings

    @property
    def registry(self) -> SillyRegistry:
        return self._registry

    def indicate(self, aiogram_user: AiogramUser) -> int:
        with self._get_session() as session:
            user = session.query(UserORM).filter_by(id=aiogram_user.id).first()
            if not user:
                user = UserORM(id=aiogram_user.id,
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

            recent_user = session.query(RecentUserORM).filter_by(id=aiogram_user.id).first()
            if not recent_user:
                recent_user = RecentUserORM(id=aiogram_user.id)
                session.add(recent_user)

            id_to_return = user.id
            session.commit()
            return id_to_return

    def get_target_message_id(self, user_id: int) -> int | None:
        with self._get_session() as session:
            return session.query(UserORM).filter_by(id=user_id).first().target_message_id

    def set_target_message_id(self, user_id: int, message_id: int):
        with self._get_session() as session:
            user = session.query(UserORM).filter_by(id=user_id).first()
            user.target_message_id = message_id
            session.commit()

    def get_current_page_name(self, user_id: int) -> str | None:
        with self._get_session() as session:
            return session.query(UserORM).filter_by(id=user_id).first().current_page_name

    def set_current_page_name(self, user_id: int, page_name: str):
        with self._get_session() as session:
            user = session.query(UserORM).filter_by(id=user_id).first()
            user.current_page_name = page_name
            session.commit()

    def init_users(self, manager: SillyManager):
        self._users = Users(self, manager)

    def summarize_statistics(self):
        with self._get_session() as session:


            current_time = datetime.now().replace(microsecond=0, minute=0, second=0)
            current_hour = session.query(StatisticsUnitORM).filter_by(ends_at=None).first()
            active_users_count = session.query(RecentUserORM).count()
            total_users_count = session.query(UserORM).count()

            if current_hour:
                if current_time > current_hour.starts_at:
                    current_hour.ends_at = current_hour.starts_at + timedelta(hours=1)
                    current_hour.active_users_count = active_users_count
                    current_hour.total_users_count = total_users_count

                    new_hour = StatisticsUnitORM(starts_at=current_time)
                    session.add(new_hour)
                    session.query(RecentUserORM).delete()

            else:
                new_hour = StatisticsUnitORM(starts_at=current_time)
                session.add(new_hour)
                session.query(RecentUserORM).delete()

            session.commit()

    def __init__(self, settings: SillySettings, *pages: SillyPage):
        super().__init__("sillygram", DECLARATIVE_BASE)
        self._io = IO()
        self._pages = Pages(*pages)
        self._settings = settings
        self._registry = SillyRegistry(self)

