from .db import SillyDB
from sqlalchemy.orm import Session


class SillyDbSection:
    _db: SillyDB

    def _get_session(self) -> Session:
        return self._db.get_session()

    def __init__(self, db: SillyDB):
        self._db = db
