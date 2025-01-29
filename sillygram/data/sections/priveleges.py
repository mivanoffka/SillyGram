from __future__ import annotations

from typing import Optional, Sequence, Tuple, TYPE_CHECKING
import logging

from ..orm import PrivelegeORM

if TYPE_CHECKING:
    from .users import SillyUser

from ..db import SillyDbSection, SillyDB
from ...privelege import SillyPrivelege
from ..settings import SillyDefaults


class Priveleges(SillyDbSection):
    _priveleges: Tuple[SillyPrivelege, ...]

    @property
    def all(self) -> Tuple[SillyPrivelege, ...]:
        return self._priveleges

    @property
    def all_names(self) -> Tuple[str, ...]:
        return tuple(privelege.name for privelege in self._priveleges)

    @property
    def master(self) -> SillyPrivelege:
        return self._priveleges[-1]

    def __getitem__(self, privelege_name: str) -> Optional[SillyPrivelege]:
        if privelege_name not in self.all_names:
            logging.warning(
                SillyDefaults.CLI.Messages.PRIVELEGE_NOT_FOUND_TEMPLATE.format(
                    privelege_name
                )
            )
            return None
        return self._priveleges[self.all_names.index(privelege_name)]

    def matches(self, user: SillyUser, privelege_name: str) -> bool:
        if user.privelege_name is None:
            return False
        if user.privelege_name not in self.all_names:
            logging.warning(
                SillyDefaults.CLI.Messages.USER_WITH_UNKNOWN_PRIVELEGE.format(
                    user.id, user.privelege_name
                )
            )
            return False
        if privelege_name not in self.all_names:
            return False

        return self.all_names.index(user.privelege_name) >= self.all_names.index(
            privelege_name
        )

    def _register(self):
        with self._get_session() as session:
            priveleges_in_db = tuple(
                privelege.name for privelege in session.query(PrivelegeORM).all()
            )
            priveleges_in_db_but_not_in_settings = set(priveleges_in_db) - set(
                self.all_names
            )
            for privelege_name in priveleges_in_db_but_not_in_settings:
                logging.warning(
                    SillyDefaults.CLI.Messages.PRIVELEGE_NOT_MENTIONED_TEMPLATE.format(
                        privelege_name
                    )
                )

            priveleges_in_settings_but_not_in_db = set(self.all_names) - set(
                priveleges_in_db
            )
            for privelege_name in priveleges_in_settings_but_not_in_db:
                session.add(PrivelegeORM(name=privelege_name))

            session.commit()

    def __init__(
        self,
        db: SillyDB,
        priveleges: Optional[Sequence[SillyPrivelege]] = None,
    ):
        super().__init__(db)
        if priveleges is None:
            self._priveleges = (
                SillyPrivelege(SillyDefaults.Names.Priveleges.MASTER),
            )
        else:
            self._priveleges = tuple(priveleges)

        self._register()
