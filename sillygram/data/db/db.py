from typing import Type
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.decl_api import DeclarativeBase

SQL_LITE_PATH_TEMPLATE = "sqlite:///{}"
RELATIVE_DB_PATH = "{}.db"


class SillyDB:
    __engine: Engine
    __session_maker: sessionmaker[Session]
    __name: str

    def get_session(self) -> Session:
        return self.__session_maker()

    def __init__(self, name: str, declarative_base: Type[DeclarativeBase]):
        self.__name = name

        self.__engine = create_engine(
            SQL_LITE_PATH_TEMPLATE.format(RELATIVE_DB_PATH.format(self.__name))
        )

        declarative_base.metadata.create_all(self.__engine)

        self.__session_maker = sessionmaker(bind=self.__engine)
