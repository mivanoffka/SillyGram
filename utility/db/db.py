import os

from config import PATH  # path to the project root
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, DeclarativeMeta

from aiogram.types import User as AiogramUser

from utility import Singleton

SQL_LITE_PATH_TEMPLATE = 'sqlite:///{}'
RELATIVE_DB_PATH = os.path.join("data", "{}.db")


class SillyDB(metaclass=Singleton):
    __engine: Engine
    __session_maker: sessionmaker
    __name: str

    def session(self):
        return self.__session_maker()

    def __init__(self, name, declarative_base):
        self.__name = name

        # Create directory if not exists
        if not os.path.exists(os.path.join(PATH, "data")):
            os.makedirs(os.path.join(PATH, "data"))

        self.__engine = create_engine(SQL_LITE_PATH_TEMPLATE.format(RELATIVE_DB_PATH.format(name)))
        declarative_base.metadata.create_all(self.__engine)
