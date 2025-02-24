from .personal import SillyPersonalRegistry
from ..db import SillyDB, SillyDbSection
from .prototype import SillyRegistryPrototype


class SillyRegistry(SillyRegistryPrototype):
    __db: SillyDB

    def __init__(self, db: SillyDB):
        super().__init__(db)
        self.__db = db

    def get_personal(self, user_id: int) -> SillyPersonalRegistry:
        return SillyPersonalRegistry(self.__db, self, user_id)
