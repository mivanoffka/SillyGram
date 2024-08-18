from typing import Dict, List

from utility import SillyDB
from .sections import Users, IO, Pages
from .types import DECLARATIVE_BASE
from ..ui import Page
from .storage import SillySettings


class Data(SillyDB):
    _users: Users
    _io: IO
    _pages: Pages
    _settings: SillySettings

    @property
    def users(self) -> Users:
        return self._users

    @property
    def io(self) -> IO:
        return self._io

    @property
    def pages(self) -> Pages:
        return self._pages

    @property
    def settings(self) -> SillySettings:
        return self._settings

    def __init__(self, settings: SillySettings, *pages: Page):
        super().__init__("sillygram", DECLARATIVE_BASE)
        self._users = Users(self)
        self._io = IO()
        self._pages = Pages(*pages)
        self._settings = settings

