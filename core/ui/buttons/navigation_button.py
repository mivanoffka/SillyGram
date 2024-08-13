from __future__ import annotations
from typing import TYPE_CHECKING

from utility import SillyText

if TYPE_CHECKING:
    from core.management.manager import SillyManager
    from core.management.event import SillyEvent

from .action_button import ActionButton


class NavigationButton(ActionButton):
    _page_name: str

    async def _show_page(self, manager: SillyManager, event: SillyEvent):
        await manager.show_page(event.user, self._page_name)

    def __init__(self, text: SillyText, page_name: str):
        super().__init__(text, self._show_page)
        self._page_name = page_name




