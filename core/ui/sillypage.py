from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Dict, List

from aiogram.types import InlineKeyboardMarkup

from . import SillyButton

# #from utility import SillyText

if TYPE_CHECKING:
    pass


class SillyPage:
    _text: str | Dict[str | Sequence[str], str]
    _name: str
    _buttons: Sequence[Sequence[SillyButton]]

    _is_home: bool = False
    _is_start: bool = False

    @property
    def text(self) -> str | Dict[str | List[str], str]:
        return self._text

    def keyboard(self, language_code: str) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[[button.aiogramify(language_code) for button in row] for row in self._buttons]
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

    def __init__(self, name: str,
                 text: str | Dict[str | Sequence[str], str],
                 buttons: SillyButton | Sequence[SillyButton] | Sequence[Sequence[SillyButton]],
                 is_home: bool = False,
                 is_start: bool = False):

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

