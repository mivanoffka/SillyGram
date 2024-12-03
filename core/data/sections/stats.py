from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from utility import SillyDbSection, SillyDB

if TYPE_CHECKING:
    from ...manager import SillyManager

from ..orm import *


class Stats(SillyDbSection):

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

    def __init__(self, db: SillyDB):
        super().__init__(db)