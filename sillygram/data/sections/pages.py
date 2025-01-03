from typing import Dict, Any, Tuple
from ..settings_and_defaults import SillyDefaults
from ...ui import SillyPage


class Pages:
    _pages: Dict[Any, SillyPage]

    @property
    def names(self) -> Tuple[str, ...]:
        return tuple(self._pages.keys())

    def get(self, name: Any) -> SillyPage:
        if name in self.names:
            return self._pages[name]

        raise KeyError("No page found with name '{}'".format(name))

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
            if page.is_start:
                start_pages.append(page)

        if len(start_pages) == 0:
            raise ValueError(f"There must be a START page.")
        elif len(start_pages) > 1:
            raise ValueError(f"There can be only one START page.")
        else:
            self._pages[SillyDefaults.Names.START_PAGE] = start_pages[0]

        home_pages = []
        for page in self._pages.values():
            if page.is_home:
                home_pages.append(page)

        if len(home_pages) == 0:
            raise ValueError(f"There must be a HOME page.")
        elif len(home_pages) > 1:
            raise ValueError(f"There can be only one HOME page.")
        else:
            self._pages[SillyDefaults.Names.HOME_PAGE] = home_pages[0]

    def __init__(self, *pages: SillyPage):
        self._pages = self._pages_to_dict(*pages)
        self._setup_specials()
