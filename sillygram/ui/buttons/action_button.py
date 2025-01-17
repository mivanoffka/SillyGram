from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Sequence, Tuple

from ...text import SillyText

if TYPE_CHECKING:
    from ...manager import SillyManager
    from ...events import SillyEvent

from ...data.settings_and_defaults import SillyDefaults

from aiogram.types import InlineKeyboardButton
from typing import List, Callable, Awaitable

from .button import SillyButton

_button_ids: List[int] = list()


class ActionSillyButton(SillyButton):
    _id: int
    _on_click: Optional[Callable[[SillyManager, SillyEvent], Awaitable[None]]]
    _priveleged: bool | str

    # region Properties etc.

    @property
    def text(self) -> SillyText:
        return self._text

    @property
    def identity(self) -> str:
        return SillyDefaults.CallbackData.BUTTON_TEMPLATE.format(self._id)

    @property
    def on_click(self) -> Callable[[SillyManager, SillyEvent], Awaitable[None]]:
        return self._on_click_wrapper

    # endregion

    # region Methods

    def aiogramify(self, language_code) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=self._text.localize(language_code), callback_data=self.identity
        )

    def _generate_id(self):
        if len(_button_ids) == 0:
            self._id = 0
            _button_ids.append(self._id)
            return

        max_id = max(_button_ids)
        self._id = max_id + 1
        _button_ids.append(self._id)

    async def _on_click_wrapper(self, manager: SillyManager, event: SillyEvent):
        async def handler(manager: SillyManager, event: SillyEvent):
            if self._on_click is not None:
                return await self._on_click(manager, event)

        @manager.priveleged(self._priveleged if isinstance(self._priveleged, str) else None)
        async def priveleged(manager: SillyManager, event: SillyEvent):
            return await handler(manager, event)

        if isinstance(self._priveleged, bool):
            if self._priveleged:
                return await priveleged(manager, event)
        elif isinstance(self._priveleged, str):
            return await priveleged(manager, event)

        return await handler(manager, event)

    # endregion

    def __init__(
        self,
        text: SillyText,
        on_click: Optional[Callable[[SillyManager, SillyEvent], Awaitable[None]]] = None,
        priveleged: bool | str = False
    ):
        super().__init__(text)
        self._generate_id()
        self._on_click = on_click
        self._priveleged = priveleged

