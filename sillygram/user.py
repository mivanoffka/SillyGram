from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from .manager import SillyManager

class SillyUser:
    _manager: SillyManager
    _id: int

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

    @property
    def nickname_or_id(self) -> int | str:
        if self.nickname:
            return self.nickname
        else:
            return self.id

    # endregion

    def __init__(self, manager: SillyManager, user_id: int):
        self._manager = manager
        self._id = user_id
