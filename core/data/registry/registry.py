from .session import SessionRegistry
from .registrable import Registrable


class SillyRegistry:
    _session: Registrable
    _constant: Registrable

    @property
    def session(self) -> Registrable:
        return self._session

    def __init__(self):
        self._session = SessionRegistry()
