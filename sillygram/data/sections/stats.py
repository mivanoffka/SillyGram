from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from ..db import SillyDbSection, SillyDB

if TYPE_CHECKING:
    from ...manager import SillyManager

from ..orm import (
    StatisticsDayORM,
    HourlyUserORM,
    StatisticsHourORM,
    StatisticsMonthORM,
    StatisticsYearORM,
    DailyUserORM,
    MonthlyUserORM,
    YearlyUserORM,
    UserORM,
)

_STATS_NOUN_LABELS = {
    StatisticsDayORM: "day",
    StatisticsHourORM: "hour",
    StatisticsMonthORM: "month",
    StatisticsYearORM: "year",
}
_STATS_ADJ_LABELS = {
    StatisticsDayORM: "daily",
    StatisticsHourORM: "hourly",
    StatisticsMonthORM: "monthly",
    StatisticsYearORM: "yearly",
}


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
        t = datetime.now().replace(
            month=1, day=1, hour=0, minute=0, second=0, microsecond=0
        )
        self._summarize(StatisticsYearORM, YearlyUserORM, t)

    def _summarize(self, statistics_unit: type, recent_user: type, t: datetime):
        with self._get_session() as session:
            current_unit = (
                session.query(statistics_unit).filter_by(ends_at=None).first()
            )
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

    def get_report(self) -> str:
        pairs = (
            (StatisticsHourORM, HourlyUserORM),
            (StatisticsDayORM, DailyUserORM),
            (StatisticsMonthORM, MonthlyUserORM),
            (StatisticsYearORM, YearlyUserORM),
        )

        total_users_count = 0
        with self._get_session() as session:
            total_users_count = session.query(UserORM).count()
        text = f"TOTAL USERS COUNT: {total_users_count}"

        text += "\n\nNEW USERS COUNT:"

        for pair in pairs:
            noun_label = _STATS_NOUN_LABELS[pair[0]]
            with self._get_session() as session:
                last_unit = (
                session.query(pair[0])
                .order_by(pair[0].ends_at.desc())
                .first()
                )
                delta = total_users_count
                if last_unit:
                    if last_unit.total_users_count:
                        delta -= last_unit.total_users_count
                text += f"\n   This {noun_label}: +{delta}"

        text += "\n\nACTIVE USERS COUNT:"

        for pair in pairs:
            with self._get_session() as session:
                active_users_count = session.query(pair[1]).count()
                text += f"\n   This {_STATS_NOUN_LABELS[pair[0]]}: {active_users_count}"

        return text

    def _get_active_users_sub_report(
        self, statistics_unit: type, recent_user: type
    ) -> str:
        adj_label = _STATS_ADJ_LABELS[statistics_unit]
        adj_label = adj_label[0].upper() + adj_label[1:]
        text = f"\n\n   {adj_label}"
        with self._get_session() as session:
            last_unit = (
                session.query(statistics_unit)
                .order_by(statistics_unit.ends_at.desc())
                .first()
            )
            if last_unit and last_unit.active_users_count:
                text += f"\n      Previous {_STATS_NOUN_LABELS[statistics_unit]}: {last_unit.active_users_count}"

            active_users_count = session.query(recent_user).count()
            text += f"\n      Current {_STATS_NOUN_LABELS[statistics_unit]}: {active_users_count}"

        return text

    def _get_total_users_sub_report(
        self, statistics_unit: type, recent_user: type
    ) -> str:
        noun_label = _STATS_NOUN_LABELS[statistics_unit]
        users_count = "?"
        with self._get_session() as session:
            users_count = session.query(recent_user).count()

        return f"\n   Last {noun_label}: +{users_count}"

    def __init__(self, db: SillyDB):
        super().__init__(db)
