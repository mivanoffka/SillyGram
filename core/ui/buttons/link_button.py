from aiogram.types import InlineKeyboardButton

from utility import SillyText
from .button import Button


class LinkButton(Button):
    _uri: str

    def aiogramify(self, language_code: str) -> any:
        return InlineKeyboardButton(text=self._text[language_code], url=self._uri)

    def __init__(self, text: SillyText, uri: str):
        super().__init__(text)
        self._uri = uri

