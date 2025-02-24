from .db import SillyDB


class SillyDbSection:
    _db: SillyDB

    def _get_session(self):
        return self._db._get_session()

    def __init__(self, db: SillyDB):
        self._db = db
