from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from .data.registry import PersonalRegistry

if TYPE_CHECKING:
    from .manager import SillyManager

class SillyUser:
    _manager: SillyManager
    _id: int
    _registry: _UserRegistry

    @property
    def registry(self) -> _UserRegistry:
        return self._registry

    class _UserRegistry:
        _disk: PersonalRegistry
        _session: PersonalRegistry

        @property
        def disk(self) -> PersonalRegistry:
            return self._disk

        @property
        def session(self) -> PersonalRegistry:
            return self._session

        def __init__(self, disk: PersonalRegistry, session: PersonalRegistry) -> None:
            self._disk = disk
            self._session = session

    # region Attributes

    @property
    def id(self) -> int:
        return self._id

    @property
    def nickname(self) -> str:
        return self._manager.users.get_nick_name(self._id)

    @property
    def last_name(self) -> str:
        return self._manager.users.get_last_name(self._id)

    @property
    def first_name(self) -> str:
        return self._manager.users.get_first_name(self._id)

    @property
    def language_code(self) -> str:
        return self._manager.users.get_language_code(self._id)

    @property
    def registration_date(self) -> datetime:
        return self._manager.users.get_registration_date(self._id)

    @property
    def last_visit_date(self) -> datetime:
        return self._manager.users.get_last_visit_date(self._id)

    @property
    def is_banned(self) -> bool:
        return self._manager.users.is_banned(self._id)

    @property
    def ban_expiration_date(self) -> Optional[datetime]:
        return self._manager.users.get_ban_expiration_date(self._id)

    @property
    def privelege_name(self) -> Optional[str]:
        return self._manager.users.get_privelege_name(self._id)

    # endregion

    def __init__(self, manager: SillyManager, user_id: int):
        self._manager = manager
        self._registry = self._UserRegistry(
            PersonalRegistry(user_id, manager.registry.disk),
            PersonalRegistry(user_id, manager.registry.session),
        )
        self._id = user_id
