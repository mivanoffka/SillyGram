from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Sequence, Tuple

from .registry.registry import SillyRegistry

from .registry import SillyPersonalRegistry, SillyDiskRegistry

if TYPE_CHECKING:
    from sillygram.manager import SillyManager

from datetime import datetime

from .db import SillyDB
from .sections import IO, Pages, Users, Stats, Priveleges
from .orm import (
    FormatArgORM,
    UserORM,
    HourlyUserORM,
    DailyUserORM,
    MonthlyUserORM,
    YearlyUserORM,
    DECLARATIVE_BASE,
)
from ..ui import SillyPage
from .settings import SillySettings


from aiogram.types import User as AiogramUser


class Data(SillyDB):
    _io: IO
    _pages: Pages
    _settings: SillySettings
    _registry: SillyDiskRegistry
    _users: Users
    _stats: Stats
    _priveleges: Priveleges

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
    
    @property
    def global_registry(self) -> SillyPersonalRegistry:
        return self._global_registry

    @property
    def stats(self) -> Stats:
        return self._stats
    
    @property
    def priveleges(self) -> Priveleges:
        return self._priveleges

    def indicate(self, aiogram_user: AiogramUser) -> int:
        with self._get_session() as session:
            user = session.query(UserORM).filter_by(id=aiogram_user.id).first()
            if not user:
                user = UserORM(
                    id=aiogram_user.id,
                    nickname=aiogram_user.username,
                    first_name=aiogram_user.first_name,
                    last_name=aiogram_user.last_name,
                    language_code=aiogram_user.language_code,
                    registered_at=datetime.now(),
                    last_seen_at=datetime.now(),
                )

                session.add(user)

            else:
                user.nickname = aiogram_user.username
                user.first_name = aiogram_user.first_name
                user.last_name = aiogram_user.last_name
                user.language_code = aiogram_user.language_code
                user.last_seen_at = datetime.now()

            self._ensure_master(session, user)
            self._save_as_recent_user(session, user.id)

            id_to_return = user.id
            session.commit()
            return id_to_return

    def _ensure_master(self, session, user: UserORM) -> None:
        if not self._settings.master_users:
            return

        for nickname_or_id in self._settings.master_users:
            if user.nickname == nickname_or_id or user.id == nickname_or_id:
                if user.privelege is None:
                    self._users.set_privelege(user.id, self._priveleges.master.name)
                else:
                    if user.privelege.name != self._priveleges.master.name:
                        self._users.set_privelege(user.id, self._priveleges.master.name)

    def _save_as_recent_user(self, session, user_id: int):
        types = (HourlyUserORM, DailyUserORM, MonthlyUserORM, YearlyUserORM)
        for user_orm in types:
            recent_user = session.query(user_orm).filter_by(id=user_id).first()
            if not recent_user:
                recent_user = user_orm(id=user_id)
                session.add(recent_user)

    def get_target_message_id(self, user_id: int) -> int | None:
        with self._get_session() as session:
            return (
                session.query(UserORM).filter_by(id=user_id).first().target_message_id
            )

    def set_target_message_id(self, user_id: int, message_id: int):
        with self._get_session() as session:
            user = session.query(UserORM).filter_by(id=user_id).first()
            user.target_message_id = message_id
            session.commit()

    def get_current_page_name(self, user_id: int) -> str | None:
        with self._get_session() as session:
            return (
                session.query(UserORM).filter_by(id=user_id).first().current_page_name
            )

    def set_current_page_name(self, user_id: int, page_name: str):
        with self._get_session() as session:
            user = session.query(UserORM).filter_by(id=user_id).first()
            user.current_page_name = page_name
            session.commit()

    def set_format_args(self, user_id: int, format_args: Optional[Sequence[str]]):
        with self._get_session() as session:
            existing_args = session.query(FormatArgORM).filter_by(user_id=user_id).all()
            for arg in existing_args:
                session.delete(arg)

            if format_args is not None:
                for arg in format_args:
                    session.add(FormatArgORM(user_id=user_id, arg=arg))
            session.commit()

    def get_format_args(self, user_id: int) -> Tuple[str, ...]:
        with self._get_session() as session:
            return tuple(
                arg.arg
                for arg in session.query(FormatArgORM).filter_by(user_id=user_id).all()
            )

    def init_users(self, manager: SillyManager):
        self._users = Users(self, manager, self._registry)

    def init_io(self, manager: SillyManager):
        self._io = IO(manager)

    def __init__(self, settings: SillySettings, *pages: SillyPage):
        super().__init__("sillygram", DECLARATIVE_BASE)
        self._pages = Pages(*pages)
        self._settings = settings
        self._registry = SillyDiskRegistry(self)
        self._global_registry = SillyPersonalRegistry(self._registry, None)
        self._stats = Stats(self)
        self._priveleges = Priveleges(self, self._settings.priveleges)
