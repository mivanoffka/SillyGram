from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData, ForeignKey

DECLARATIVE_BASE = declarative_base()


class User(DECLARATIVE_BASE):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    target_message_id = Column(Integer, nullable=True)
    current_page_name = Column(String, nullable=True)

    nickname = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    language_code = Column(String, nullable=True)

