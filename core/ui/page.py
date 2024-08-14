from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List, Sequence

# #from utility import SillyText

if TYPE_CHECKING:
    pass

from .keyboard import Keyboard


class Page:
    _text: str | Dict[str | Sequence[str], str]
    _keyboard: Keyboard
    _name: str

    _is_home: bool = False
    _is_start: bool = False

    @property
    def text(self) -> str | Dict[str | List[str], str]:
        return self._text

    @property
    def keyboard(self) -> Keyboard:
        return self._keyboard

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
                 keyboard: Keyboard,
                 is_home: bool = False,
                 is_start: bool = False):

        self._name = name
        self._text = text
        self._keyboard = keyboard

        self._is_home = is_home
        self._is_start = is_start

