from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime


class DECLARATIVE_BASE(DeclarativeBase):
    pass


class UserORM(DECLARATIVE_BASE):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    privilege_id: Mapped[int | None] = mapped_column(
        ForeignKey("privileges.id"), nullable=True
    )

    target_message_id: Mapped[int | None] = mapped_column(nullable=True)
    current_page_name: Mapped[str | None] = mapped_column(nullable=True)

    nickname: Mapped[str | None] = mapped_column(nullable=True)
    first_name: Mapped[str | None] = mapped_column(nullable=True)
    last_name: Mapped[str | None] = mapped_column(nullable=True)
    language_code: Mapped[str | None] = mapped_column(nullable=True)

    registered_at: Mapped[datetime | None] = mapped_column(nullable=True)
    last_seen_at: Mapped[datetime | None] = mapped_column(nullable=True)

    privilege: Mapped["PrivilegeORM"] = relationship(
        "PrivilegeORM", back_populates="users"
    )

    local_values: Mapped[list["RegistryValueORM"]] = relationship(
        "RegistryValueORM", back_populates="user"
    )

    format_args: Mapped[list["FormatArgORM"]] = relationship(
        "FormatArgORM", back_populates="user"
    )

    @property
    def all_args(self) -> list[str]:
        return [format_arg.arg for format_arg in self.format_args]


class FormatArgORM(DECLARATIVE_BASE):
    __tablename__ = "format_args"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    arg: Mapped[str] = mapped_column(nullable=False)

    user: Mapped[UserORM] = relationship("UserORM", back_populates="format_args")


class PrivilegeORM(DECLARATIVE_BASE):
    __tablename__ = "privileges"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    users: Mapped[list[UserORM]] = relationship("UserORM", back_populates="privilege")


class BanORM(DECLARATIVE_BASE):
    __tablename__ = "bans"

    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    expires: Mapped[datetime | None] = mapped_column(nullable=True)


class RegistryValueORM(DECLARATIVE_BASE):
    __tablename__ = "registry_values"

    key_name: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    value: Mapped[str] = mapped_column()

    user: Mapped["UserORM"] = relationship("UserORM", back_populates="local_values")


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
    __tablename__ = "hourly_users"
    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)


class DailyUserORM(DECLARATIVE_BASE):
    __tablename__ = "daily_users"
    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)


class MonthlyUserORM(DECLARATIVE_BASE):
    __tablename__ = "monthly_users"
    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)


class YearlyUserORM(DECLARATIVE_BASE):
    __tablename__ = "yearly_users"
    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
