from __future__ import annotations

from calendar import weekday
from typing import TYPE_CHECKING

from sqlalchemy import desc

if TYPE_CHECKING:
    from core.manager import SillyManager

from datetime import datetime, timedelta

from utility import SillyDB
from .sections import IO, Pages, Users
from .orm import *
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

            self._save_as_recent_user(session, user.id)

            id_to_return = user.id
            session.commit()
            return id_to_return

    def _save_as_recent_user(self, session, user_id: int):
        types = (HourlyUserORM, DailyUserORM, MonthlyUserORM, YearlyUserORM)
        for user_orm in types:
            recent_user = session.query(user_orm).filter_by(id=user_id).first()
            if not recent_user:
                recent_user = user_orm(id=user_id)
                session.add(recent_user)

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

    async def summarize_hourly_statistics(self, manager: SillyManager):
        t = datetime.now().replace(microsecond=0, minute=0, second=0)
        self._summarize(StatisticsHourORM, HourlyUserORM, t)

    async def summarize_daily_statistics(self, manager: SillyManager):
        t = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self._summarize(StatisticsDayORM, DailyUserORM, t)

    async def summarize_monthly_statistics(self, manager: SillyManager):
        t = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        self._summarize(StatisticsMonthORM, MonthlyUserORM, t)

    async def summarize_yearly_statistics(self, manager: SillyManager):
        t = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        self._summarize(StatisticsYearORM, YearlyUserORM, t)

    def _summarize(self, statistics_unit: type, recent_user: type, t: datetime):
        with self._get_session() as session:
            current_unit = session.query(statistics_unit).filter_by(ends_at=None).first()
            active_users_count = session.query(recent_user).count()
            total_users_count = session.query(UserORM).count()

            if current_unit:
                if t > current_unit.starts_at:
                    current_unit.ends_at = current_unit.starts_at + timedelta(hours=1)
                    current_unit.active_users_count = active_users_count
                    current_unit.total_users_count = total_users_count

                    new_unit = statistics_unit(starts_at=t)
                    session.add(new_unit)
                    session.query(recent_user).delete()

            else:
                new_unit = statistics_unit(starts_at=t)
                session.add(new_unit)
                session.query(recent_user).delete()

            session.commit()

    def __init__(self, settings: SillySettings, *pages: SillyPage):
        super().__init__("sillygram", DECLARATIVE_BASE)
        self._io = IO()
        self._pages = Pages(*pages)
        self._settings = settings
        self._registry = SillyRegistry(self)

