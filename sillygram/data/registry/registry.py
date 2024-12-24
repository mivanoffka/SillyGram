from ...utility import SillyDB
from .disk import DiskRegistry
from .session import SessionRegistry
from .registrable import Registrable


class SillyRegistry:
    _session: Registrable
    _disk: Registrable

    @property
    def session(self) -> Registrable:
        return self._session

    @property
    def disk(self) -> Registrable:
        return self._disk

    def __init__(self, db: SillyDB):
        self._session = SessionRegistry()
        self._disk = DiskRegistry(db)
