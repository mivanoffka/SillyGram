from typing import Dict, Any, Sequence

from aiogram.types import InlineKeyboardButton

from utility import localize
from .sillybutton import SillyButton


class LinkButton(SillyButton):
    _uri: str

    def aiogramify(self, language_code: str) -> Any:
        return InlineKeyboardButton(
            text=localize(self._text, language_code), url=self._uri
        )

    def __init__(self, text: str | Dict[str | Sequence[str], str], uri: str):
        super().__init__(text)
        self._uri = uri
