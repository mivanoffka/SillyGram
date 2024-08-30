from utility import SillyDB
from .sections import Users, IO, Pages
from .types import DECLARATIVE_BASE
from ..ui import SillyPage
from .settings_and_defaults import SillySettings
from .registry import SillyRegistry


class Data(SillyDB):
    _users: Users
    _io: IO
    _pages: Pages
    _settings: SillySettings
    _registry: SillyRegistry

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

    @property
    def registry(self) -> SillyRegistry:
        return self._registry

    def __init__(self, settings: SillySettings, *pages: SillyPage):
        super().__init__("sillygram", DECLARATIVE_BASE)
        self._users = Users(self)
        self._io = IO()
        self._pages = Pages(*pages)
        self._settings = settings
        self._registry = SillyRegistry(self)

