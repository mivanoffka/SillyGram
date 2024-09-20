from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..manager import SillyManager

from collections.abc import Sequence
from typing import Optional, Callable, Awaitable, List
from .activity import SillyRegularActivity
from datetime import time, date, datetime, timedelta


class SillyDateTimeActivity(SillyRegularActivity):
    _executed_today: List[time]
    _last_check_date: date

    async def _activity(self, manager: SillyManager):
        raise NotImplementedError()

    async def _condition(self, manager):
        current = datetime.now()
        if self._last_check_date != current.date():
            self._executed_today.clear()
        self._last_check_date = current.date()
        result = self._matches_time(current) and self._matches_date(current)
        return result

    def _matches_time(self, date_time: datetime) -> bool:
        for allowed_time in self._times:
            if allowed_time in self._executed_today:
                continue
            if date_time.time() >= allowed_time:
                if self._max_time_delta:
                    allowed_datetime = datetime(year=date_time.year,
                                                month=date_time.month,
                                                day=date_time.day,
                                                hour=allowed_time.hour,
                                                minute=allowed_time.minute)
                    if date_time - allowed_datetime <= timedelta(seconds=self._max_time_delta.total_seconds()):
                        self._executed_today.append(allowed_time)
                        return True

                else:
                    self._executed_today.append(allowed_time)
                    return True

        return False

    def _matches_date(self, date_time: datetime) -> bool:
        matches_year = date_time.year in self._years if self._years else True
        matches_month = date_time.month in self._months if self._months else True
        matches_day = date_time.day in self._days_of_month if self._days_of_month else True
        matches_weekday = date_time.weekday() in self._days_of_week if self._days_of_week else True

        return matches_year and matches_month and matches_day and matches_weekday

    def __init__(self,
                 activity: Callable[[SillyManager], Awaitable[None]],
                 times: Sequence[time] | time,
                 monthdays: Optional[Sequence[int] | int] = None,
                 weekdays: Optional[Sequence[int] | int] = None,
                 months: Optional[Sequence[int] | int] = None,
                 years: Optional[Sequence[int] | int] = None,
                 max_time_delta: Optional[timedelta] = None):

        self._executed_today = []
        self._activity = activity
        self._last_check_date = datetime.now().date()

        self._times = times if isinstance(times, Sequence) else (times, )

        self._days_of_month = monthdays if isinstance(monthdays, Sequence) else (monthdays,) if monthdays else ()
        self._days_of_week = weekdays if isinstance(weekdays, Sequence) else (weekdays,) if weekdays else ()
        self._months = months if isinstance(months, Sequence) else (months, ) if months else ()
        self._years = years if isinstance(years, Sequence) else (years, ) if years else ()

        self._max_time_delta = max_time_delta
