from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Tuple, Dict, Any

if TYPE_CHECKING:
    from ...manager import SillyManager
    from ...events import SillyEvent

from .action_button import SillyActionButton
from ...text import SillyText


class SillyNavigationButton(SillyActionButton):
    _page_name: str
    _not_found_message: Optional[SillyText]

    _f_args: Optional[Tuple]
    _f_kwargs: Optional[Dict[str, Any]]

    async def _show_page(self, manager: SillyManager, event: SillyEvent):
        await manager.show_page(
            event.user,
            self._page_name,
            not_found_message=self._not_found_message,
            f_args=self._f_args,
            f_kwargs=self._f_kwargs,
        )

    def __init__(
        self,
        text: SillyText,
        page_name: str,
        priveleged: bool | str = False,
        not_found_message: Optional[SillyText] = None,
        f_args: Optional[Tuple] = None,
        f_kwargs: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(text, self._show_page, priveleged)
        self._page_name = page_name
        self._not_found_message = not_found_message
        self._f_args = f_args
        self._f_kwargs = f_kwargs
