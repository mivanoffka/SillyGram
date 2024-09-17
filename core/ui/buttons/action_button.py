from __future__ import annotations
from typing import TYPE_CHECKING

#from utility import SillyText

if TYPE_CHECKING:
    from ...manager import SillyManager
    from ...user import SillyUser

from ...data.settings_and_defaults import SillyDefaults

from aiogram.types import InlineKeyboardButton
from typing import List, Callable, Awaitable, Dict, Sequence

from .sillybutton import SillyButton
from utility import localize

_button_ids: List[int] = list()


class ActionButton(SillyButton):
    _id: int
    _on_click: Callable[[SillyManager, SillyUser], Awaitable[None]]

    # region Properties etc.

    @property
    def text(self) -> str | Dict[str | List[str], str]:
        return self._text

    @property
    def identity(self) -> str:
        return SillyDefaults.CallbackData.BUTTON_TEMPLATE.format(self._id)

    @property
    def on_click(self) -> Callable[[SillyManager, SillyUser], Awaitable[None]]:
        return self._on_click_wrapper

    # endregion

    # region Methods

    def aiogramify(self, language_code) -> InlineKeyboardButton:
        return InlineKeyboardButton(text=localize(self._text, language_code), callback_data=self.identity)

    def _generate_id(self):
        if len(_button_ids) == 0:
            self._id = 0
            _button_ids.append(self._id)
            return

        max_id = max(_button_ids)
        self._id = max_id + 1
        _button_ids.append(self._id)

    async def _on_click_wrapper(self, manager: SillyManager, user: SillyUser):
        if self._on_click is not None:
            await self._on_click(manager, user)

    # endregion

    def __init__(self,
                 text: str | Dict[str | Sequence[str], str],
                 on_click: Callable[[SillyManager, SillyUser], Awaitable[None]] = None):
        super().__init__(text)
        self._generate_id()
        self._on_click = on_click

