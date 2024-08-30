from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.orm import relationship

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

    registered_at = Column(DateTime, nullable=True)
    last_seen_at = Column(DateTime, nullable=True)

    local_values = relationship("RegistryValue", back_populates="user")


class RegistryKey(DECLARATIVE_BASE):
    __tablename__ = 'registry_keys'

    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=False)
    global_value = Column(String, nullable=True)
    local_values = relationship("RegistryValue", back_populates="key")


class RegistryValue(DECLARATIVE_BASE):
    __tablename__ = 'registry_values'

    id = Column(Integer, primary_key=True)
    key_id = Column(Integer, ForeignKey('registry_keys.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    value = Column(String, nullable=True)

    key = relationship("RegistryKey", back_populates="local_values")
    user = relationship("User", back_populates="local_values")



