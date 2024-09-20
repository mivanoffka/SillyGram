from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.orm import relationship

DECLARATIVE_BASE = declarative_base()


class UserORM(DECLARATIVE_BASE):
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

    local_values = relationship("RegistryValueORM", back_populates="user")


class AdminORM(DECLARATIVE_BASE):
    __tablename__ = 'admins'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)


class BanORM(DECLARATIVE_BASE):
    __tablename__ = 'bans'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    expires = Column(DateTime, nullable=True)


class RegistryKeyORM(DECLARATIVE_BASE):
    __tablename__ = 'registry_keys'

    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=False)
    global_value = Column(String, nullable=True)
    local_values = relationship("RegistryValueORM", back_populates="key")


class RegistryValueORM(DECLARATIVE_BASE):
    __tablename__ = 'registry_values'

    id = Column(Integer, primary_key=True)
    key_id = Column(Integer, ForeignKey('registry_keys.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    value = Column(String, nullable=True)

    key = relationship("RegistryKeyORM", back_populates="local_values")
    user = relationship("UserORM", back_populates="local_values")


class StatisticsUnitORM(DECLARATIVE_BASE):
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True)

    active_users_count = Column(Integer, nullable=True)
    total_users_count = Column(Integer, nullable=True)

    starts_at = Column(DateTime, nullable=False)
    ends_at = Column(DateTime, nullable=True)

class RecentUserORM(DECLARATIVE_BASE):
    __tablename__ = 'recent_users'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)


