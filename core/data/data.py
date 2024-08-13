from utility import SillyDB
from .sections import Users, Session, Pages
from .types import DECLARATIVE_BASE
from ..ui import Page
from .storage import SillySettings


class Data(SillyDB):
    _users: Users
    _session: Session
    _pages: Pages
    _settings: SillySettings

    @property
    def users(self) -> Users:
        return self._users

    @property
    def session(self) -> Session:
        return self._session

    @property
    def pages(self) -> Pages:
        return self._pages

    @property
    def settings(self) -> SillySettings:
        return self._settings

    def __init__(self, settings: SillySettings, *pages: Page):
        super().__init__("sillygram", DECLARATIVE_BASE)
        self._users = Users(self)
        self._session = Session(self)
        self._pages = Pages(*pages)
        self._settings = settings

