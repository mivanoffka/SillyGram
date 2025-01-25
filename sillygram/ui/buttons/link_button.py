from typing import Any

from aiogram.types import InlineKeyboardButton

from ...text import SillyText
from .button import SillyButton


class SillyLinkButton(SillyButton):
    _uri: str

    def aiogramify(self, language_code: str) -> Any:
        return InlineKeyboardButton(
            text=self._text.localize(language_code), url=self._uri
        )

    def __init__(self, text: SillyText, uri: str):
        super().__init__(text)
        self._uri = uri
