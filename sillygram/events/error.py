from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Tuple

from .event import SillyEvent

if TYPE_CHECKING:
    from .. import SillyUser

class SillyErrorEvent(SillyEvent):
    @property
    def exception(self) -> Exception:
        return self._kwargs["exception"]
    
    def __init__(self, user: SillyUser, exception: Exception, *args, **kwargs):
        super().__init__(user, exception=exception, *args, **kwargs)