from __future__ import annotations

from typing import Optional, Sequence, Tuple, TYPE_CHECKING
import logging

from ..orm import PrivilegeORM

if TYPE_CHECKING:
    from .users import SillyUser

from ..db import SillyDbSection, SillyDB
from ...privilege import SillyPrivilege
from ..settings import SillyDefaults


class Privileges(SillyDbSection):
    _privileges: Tuple[SillyPrivilege, ...]

    @property
    def all(self) -> Tuple[SillyPrivilege, ...]:
        return self._privileges

    @property
    def all_names(self) -> Tuple[str, ...]:
        return tuple(privilege.name for privilege in self._privileges)

    @property
    def master(self) -> SillyPrivilege:
        return self._privileges[-1]

    def __getitem__(self, privilege_name: str) -> Optional[SillyPrivilege]:
        if privilege_name not in self.all_names:
            logging.warning(
                SillyDefaults.CLI.Messages.PRIVILEGE_NOT_FOUND_TEMPLATE.format(
                    privilege_name
                )
            )
            return None
        return self._privileges[self.all_names.index(privilege_name)]

    def matches(self, user: SillyUser, privilege_name: str) -> bool:
        if user.privilege_name is None:
            return False
        if user.privilege_name not in self.all_names:
            logging.warning(
                SillyDefaults.CLI.Messages.USER_WITH_UNKNOWN_PRIVILEGE.format(
                    user.id, user.privilege_name
                )
            )
            return False
        if privilege_name not in self.all_names:
            return False

        return self.all_names.index(user.privilege_name) >= self.all_names.index(
            privilege_name
        )

    def _register(self):
        with self._get_session() as session:
            privileges_in_db = tuple(
                privilege.name for privilege in session.query(PrivilegeORM).all()
            )
            privileges_in_db_but_not_in_settings = set(privileges_in_db) - set(
                self.all_names
            )
            for privilege_name in privileges_in_db_but_not_in_settings:
                logging.warning(
                    SillyDefaults.CLI.Messages.PRIVILEGE_NOT_MENTIONED_TEMPLATE.format(
                        privilege_name
                    )
                )

            privileges_in_settings_but_not_in_db = set(self.all_names) - set(
                privileges_in_db
            )
            for privilege_name in privileges_in_settings_but_not_in_db:
                session.add(PrivilegeORM(name=privilege_name))

            session.commit()

    def __init__(
        self,
        db: SillyDB,
        privileges: Optional[Sequence[SillyPrivilege]] = None,
    ):
        super().__init__(db)
        if privileges is None:
            self._privileges = (SillyPrivilege(SillyDefaults.Names.PRIVILEGEs.MASTER),)
        else:
            self._privileges = tuple(privileges)

        self._register()
