from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Tuple

if TYPE_CHECKING:
    from . import SillyUser

class SillyEvent:
    _user: SillyUser
    _args: Tuple
    _kwargs: Dict
    
    @property
    def user(self) -> SillyUser:
        return self._user
    
    @property
    def args(self) -> Tuple:
        return self._args
    
    @property
    def kwargs(self) -> Dict:
        return self._kwargs
    
    def __init__(self, user: SillyUser, *args, **kwargs):
        self._user = user
        self._args = args
        self._kwargs = kwargs