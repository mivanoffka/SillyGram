from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Awaitable, Callable, Optional, Tuple

from aiogram.types import InlineKeyboardMarkup


from ..text import SillyText

from . import SillyButton

if TYPE_CHECKING:
    from ..events import SillyEvent
    from ..manager import SillyManager


class SillyPage:
    _text: SillyText
    _name: str
    _buttons: Sequence[Sequence[SillyButton]]

    _is_home: bool = False
    _is_start: bool = False
    
    _on_opened: Callable[[SillyManager, SillyEvent], Awaitable[Optional[Tuple[str, ...]]]]
    
    @property
    def text(self) -> SillyText:
        return self._text

    def keyboard(self, language_code: str) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [button.aiogramify(language_code) for button in row]
                for row in self._buttons
            ]
        )

    @property
    def buttons(self):
        return tuple(button for row in self._buttons for button in row)

    @property
    def is_home(self) -> bool:
        return self._is_home

    @property
    def is_start(self) -> bool:
        return self._is_start

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def on_opened(self) -> Callable[[SillyManager, SillyEvent], Awaitable[Optional[Tuple[str, ...]]]]:
        return self._on_opened

    def __init__(
        self,
        name: str,
        text: SillyText,
        buttons: SillyButton | Sequence[SillyButton] | Sequence[Sequence[SillyButton]],
        on_opened: Optional[Callable[[SillyManager, SillyEvent], Awaitable[Optional[Tuple[str, ...]]]]] = None,
        is_home: bool = False,
        is_start: bool = False,
    ):

        buttons_edited = []
        row = []

        if isinstance(buttons, SillyButton):
            buttons_edited = [[buttons]]
        if isinstance(buttons, Sequence):
            for x in buttons:
                if isinstance(x, SillyButton):
                    buttons_edited.append(row)
                    row = []
                    buttons_edited.append([x])
                if isinstance(x, Sequence):
                    if row:
                        buttons_edited.append(row)
                    row = []
                    for y in x:
                        row.append(y)

        if row:
            buttons_edited.append(row)

        self._name = name
        self._text = text
        self._buttons = buttons_edited

        self._is_home = is_home
        self._is_start = is_start
        
        async def format_default(manager: SillyManager, event: SillyEvent):
            return (*event.args, *event.kwargs.values())
        
        self._on_opened = on_opened if on_opened else format_default
