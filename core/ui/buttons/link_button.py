from typing import Dict, List, Sequence

from aiogram.types import InlineKeyboardButton

#from utility import SillyText
from .sillybutton import SillyButton


class LinkButton(SillyButton):
    _uri: str

    def aiogramify(self, language_code: str) -> any:
        return InlineKeyboardButton(text=self._text[language_code], url=self._uri)

    def __init__(self, text: str | Dict[str | Sequence[str], str], uri: str):
        super().__init__(text)
        self._uri = uri

