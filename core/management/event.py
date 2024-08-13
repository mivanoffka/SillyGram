from core.data import SillyUser
from typing import Tuple, Dict


class SillyEvent:
    _user_info: SillyUser
    _args: Tuple
    _kwargs: Dict

    @property
    def args(self) -> Tuple:
        return self._args

    @property
    def kwargs(self) -> Dict:
        return self._kwargs

    @property
    def user(self) -> SillyUser:
        return self._user_info

    def __init__(self, user: SillyUser, *args, **kwargs) -> None:
        self._user_info = user
        self._args = args
        self._kwargs = kwargs

