from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Optional, Any

from .data.registry import PersonalRegistry

if TYPE_CHECKING:
    from .manager import SillyManager
    from .text import SillyText


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
    def is_admin(self) -> bool:
        return self._manager.users.is_admin(self._id)

    @property
    def ban_expiration_date(self) -> Optional[datetime]:
        return self._manager.users.get_ban_expiration_date(self._id)

    # endregion

    # region Status actions

    def ban(self, duration: timedelta):
        self._manager.users.ban(self._id, duration)

    def unban(self, duration: timedelta):
        self._manager.users.unban(self._id)

    def promote(self):
        self._manager.users.promote(self._id)

    def demote(self):
        self._manager.users.demote(self._id)

    # endregion

    # region Messenger actions

    async def show_notification(self, text: SillyText):
        await self._manager.show_notification(self, text)

    async def show_interruption(self, text: SillyText):
        await self._manager.show_interruption(self, text)

    async def show_banner(self, text: SillyText):
        await self._manager.show_banner(self, text)

    async def show_message(self, text: SillyText):
        await self._manager.show_message(self, text)

    async def goto_page(self, page_name: Any, new_target_message=False):
        await self._manager.show_page(self, page_name, new_target_message)

    async def refresh_page(self):
        await self._manager.refresh_page(self)

    async def get_input(
        self, prompt: SillyText
    ) -> str | None:
        return await self._manager.get_input(self, prompt)

    async def show_dialog(
        self,
        question: SillyText,
        *dialog_options: SillyText,
    ) -> int | None:
        return await self._manager.show_dialog(self, question, *dialog_options)

    async def get_yes_no(self, question: SillyText):
        return await self._manager.get_yes_no_answer(self, question)

    # endregion

    def __init__(self, manager: SillyManager, user_id: int):
        self._manager = manager
        self._registry = self._UserRegistry(
            PersonalRegistry(user_id, manager.registry.disk),
            PersonalRegistry(user_id, manager.registry.session),
        )
        self._id = user_id
