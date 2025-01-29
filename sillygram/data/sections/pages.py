from enum import Enum
import logging
from typing import Dict, Any, Tuple, Optional
from ..settings import SillyDefaults
from ...ui import SillyPage


class Pages:
    _pages: Dict[Any, SillyPage]

    @property
    def names(self) -> Tuple[str, ...]:
        return tuple(self._pages.keys())

    def get(self, name: Any) -> Optional[SillyPage]:
        if name in self.names:
            return self._pages[name]

        return None

    @staticmethod
    def _pages_to_dict(*pages: SillyPage) -> Dict[Any, SillyPage]:
        pages_dict = {}
        for page in pages:
            if page.name in pages_dict.keys():
                raise ValueError(f"Page named {page.name} already exists")
            if page in pages_dict.values():
                continue
            pages_dict[page.name] = page

        return pages_dict

    def _setup_specials(self):
        start_pages = []
        for page in self._pages.values():
            if page.flags & SillyPage.Flags.START:
                start_pages.append(page)

        if len(start_pages) == 0:
            logging.warning("There must be a START page.")
        else:
            if len(start_pages) > 1:
                logging.warning("There should beonly one START page.")

            self._pages[SillyPage.Pointers.START] = start_pages[0]

        home_pages = []
        for page in self._pages.values():
            if page.flags & SillyPage.Flags.HOME:
                home_pages.append(page)

        if len(home_pages) == 0:
            logging.warning("There must be a HOME page.")
        else:
            if len(home_pages) > 1:
                logging.warning("There should be only one HOME page.")
            self._pages[SillyPage.Pointers.HOME] = home_pages[0]

        options_pages = []
        for page in self._pages.values():
            if page.flags & SillyPage.Flags.OPTIONS:
                options_pages.append(page)

        if len(options_pages) > 0:
            if len(options_pages) > 1:
                logging.warning("There should be only one OPTIONS page.")
            self._pages[SillyPage.Pointers.ADDITIONAL_OPTIONS] = options_pages[0]

    def __init__(self, *pages: SillyPage):
        self._pages = self._pages_to_dict(*pages)
        self._setup_specials()
