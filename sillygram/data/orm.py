from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime


class DECLARATIVE_BASE(DeclarativeBase):
    pass

class UserORM(DECLARATIVE_BASE):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    target_message_id: Mapped[int | None] = mapped_column(nullable=True)
    current_page_name: Mapped[str | None] = mapped_column(nullable=True)

    nickname: Mapped[str | None] = mapped_column(nullable=True)
    first_name: Mapped[str | None] = mapped_column(nullable=True)
    last_name: Mapped[str | None] = mapped_column(nullable=True)
    language_code: Mapped[str | None] = mapped_column(nullable=True)

    registered_at: Mapped[datetime | None] = mapped_column(nullable=True)
    last_seen_at: Mapped[datetime | None] = mapped_column(nullable=True)

    local_values: Mapped[list["RegistryValueORM"]] = relationship(
        "RegistryValueORM", back_populates="user"
    )

class AdminORM(DECLARATIVE_BASE):
    __tablename__ = 'admins'
    
    id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)

class BanORM(DECLARATIVE_BASE):
    __tablename__ = 'bans'

    id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    expires: Mapped[datetime | None] = mapped_column(nullable=True)

class RegistryKeyORM(DECLARATIVE_BASE):
    __tablename__ = 'registry_keys'

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(nullable=False)
    global_value: Mapped[str | None] = mapped_column(nullable=True)
    
    local_values: Mapped[list["RegistryValueORM"]] = relationship(
        "RegistryValueORM", back_populates="key"
    )

class RegistryValueORM(DECLARATIVE_BASE):
    __tablename__ = 'registry_values'

    id: Mapped[int] = mapped_column(primary_key=True)
    key_id: Mapped[int] = mapped_column(ForeignKey('registry_keys.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    value: Mapped[str | None] = mapped_column(nullable=True)

    key: Mapped["RegistryKeyORM"] = relationship("RegistryKeyORM", back_populates="local_values")
    user: Mapped["UserORM"] = relationship("UserORM", back_populates="local_values")

# region Statistics

# region Statistics

class StatisticsHourORM(DECLARATIVE_BASE):
    __tablename__ = "statistics_hour"

    id: Mapped[int] = mapped_column(primary_key=True)

    active_users_count: Mapped[int | None] = mapped_column(nullable=True)
    total_users_count: Mapped[int | None] = mapped_column(nullable=True)

    starts_at: Mapped[datetime] = mapped_column(nullable=False)
    ends_at: Mapped[datetime | None] = mapped_column(nullable=True)


class StatisticsDayORM(DECLARATIVE_BASE):
    __tablename__ = "statistics_day"

    id: Mapped[int] = mapped_column(primary_key=True)

    active_users_count: Mapped[int | None] = mapped_column(nullable=True)
    total_users_count: Mapped[int | None] = mapped_column(nullable=True)

    starts_at: Mapped[datetime] = mapped_column(nullable=False)
    ends_at: Mapped[datetime | None] = mapped_column(nullable=True)

class StatisticsMonthORM(DECLARATIVE_BASE):
    __tablename__ = "statistics_month"

    id: Mapped[int] = mapped_column(primary_key=True)

    active_users_count: Mapped[int | None] = mapped_column(nullable=True)
    total_users_count: Mapped[int | None] = mapped_column(nullable=True)

    starts_at: Mapped[datetime] = mapped_column(nullable=False)
    ends_at: Mapped[datetime | None] = mapped_column(nullable=True)

class StatisticsYearORM(DECLARATIVE_BASE):
    __tablename__ = "statistics_year"

    id: Mapped[int] = mapped_column(primary_key=True)

    active_users_count: Mapped[int | None] = mapped_column(nullable=True)
    total_users_count: Mapped[int | None] = mapped_column(nullable=True)

    starts_at: Mapped[datetime] = mapped_column(nullable=False)
    ends_at: Mapped[datetime | None] = mapped_column(nullable=True)

# endregion

class HourlyUserORM(DECLARATIVE_BASE):
    __tablename__ = 'hourly_users'
    id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)

class DailyUserORM(DECLARATIVE_BASE):
    __tablename__ = 'daily_users'
    id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)

class MonthlyUserORM(DECLARATIVE_BASE):
    __tablename__ = 'monthly_users'
    id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)

class YearlyUserORM(DECLARATIVE_BASE):
    __tablename__ = 'yearly_users'
    id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)