from typing import Any
from aiogram.types import InlineKeyboardButton

from ...text import SillyText


class SillyButton:
    _text: SillyText

    @property
    def text(self) -> SillyText:
        return self._text

    def aiogramify(self, language_code: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(text=self._text.localize(language_code))

    def __init__(self, text: SillyText):
        self._text = text
