from typing import Sequence

from .aiogramable import Aiogramable
from aiogram.types import InlineKeyboardMarkup
from .buttons import Button


class Keyboard(Aiogramable):
    _buttons: Sequence[Sequence[Button]]

    def __init__(self, *buttons: Sequence[Button]) -> None:
        self._buttons = buttons

    def aiogramify(self, language_code: str) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[[button.aiogramify(language_code) for button in row] for row in self._buttons]
        )

    @property
    def buttons(self) -> Sequence[Button]:
        return tuple(button for row in self._buttons for button in row)


