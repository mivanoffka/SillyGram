from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Tuple, Any

if TYPE_CHECKING:
    from .. import SillyUser


class SillyEvent:
    _user: SillyUser
    _args: Tuple[Any, ...]
    _kwargs: Dict[str, Any]

    @property
    def user(self) -> SillyUser:
        return self._user

    @property
    def args(self) -> Tuple[Any, ...]:
        return self._args

    @property
    def kwargs(self) -> Dict[str, Any]:
        return self._kwargs

    def __init__(self, user: SillyUser, *args: Any, **kwargs: Any):
        self._user = user
        self._args = args
        self._kwargs = kwargs
