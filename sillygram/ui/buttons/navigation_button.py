from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...manager import SillyManager
    from ...events import SillyEvent
    
from .action_button import ActionSillyButton
from ...text import SillyText


class NavigationSillyButton(ActionSillyButton):
    _page_name: str

    async def _show_page(self, manager: SillyManager, event: SillyEvent):
        await manager.show_page(event.user, self._page_name)

    def __init__(self, text: SillyText, page_name: str):
        super().__init__(text, self._show_page)
        self._page_name = page_name
