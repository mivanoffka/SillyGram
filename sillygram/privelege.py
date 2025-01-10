from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .text import SillyText


class SillyPrivelege:
    _name: str
    _message: Optional[SillyText]
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def message(self) -> Optional[SillyText]:
        return self._message
    
    def __init__(self, name: str, message: Optional[SillyText] = None):
        self._name = name
        self._message = message