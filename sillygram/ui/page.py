from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional, Tuple, Self

from aiogram.types import InlineKeyboardMarkup
from enum import Flag, auto

from ..data.settings.defaults import SillyDefaults

from ..text import SillyText

from . import SillyButton

if TYPE_CHECKING:
    from ..events import SillyEvent
    from ..manager import SillyManager


class SillyPage:
    class Pointers:
        START = SillyDefaults.Names.Pages.START
        HOME = SillyDefaults.Names.Pages.HOME
        CONTROLS = SillyDefaults.Names.Pages.CONTROLS
        CUSTOM_CONTROLS = SillyDefaults.Names.Pages.CUSTOM_CONTROLS

    class Flags(Flag):
        NO = 0
        HOME = auto()
        START = auto()
        CUSTOM_CONTROLS = auto()

        def __or__(self, other: Self):
            if (
                self is SillyPage.Flags.CUSTOM_CONTROLS
                or other is SillyPage.Flags.CUSTOM_CONTROLS
            ):
                if self != SillyPage.Flags.NO and other != SillyPage.Flags.NO:
                    raise ValueError(
                        SillyDefaults.CLI.Messages.CUSTOM_CONTROLS_FLAG_INCOMPATIBLE
                    )

            return super().__or__(other)

    _text: SillyText
    _name: str
    _buttons: Sequence[Sequence[SillyButton]]
    _privileged: bool | str

    _flags: Flags

    _get_format_args: Callable[
        [SillyManager, SillyEvent], Awaitable[Optional[Tuple[str, ...]]]
    ]

    @property
    def text(self) -> SillyText:
        return self._text

    def keyboard(self, language_code: str) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [button.aiogramify(language_code) for button in row]
                for row in self._buttons
            ]
        )

    @property
    def buttons(self):
        return tuple(button for row in self._buttons for button in row)

    @property
    def flags(self) -> Flags:
        return self._flags

    @property
    def name(self) -> str:
        return self._name

    @property
    def privileged(self) -> str | bool:
        return self._privileged

    async def get_format_args(self, manager: SillyManager, event: SillyEvent):
        args = event.args
        kwargs = event.kwargs.values()
        if len(args) > 0 or len(kwargs) > 0:
            return (
                *args,
                *kwargs,
            )
        else:
            return await self._get_format_args(manager, event)

    def __init__(
        self,
        name: str,
        text: SillyText,
        buttons: Optional[
            SillyButton | Sequence[SillyButton] | Sequence[Sequence[SillyButton]]
        ] = None,
        privileged: bool | str = False,
        get_format_args: Optional[
            Callable[[SillyManager, SillyEvent], Awaitable[Optional[Tuple[Any, ...]]]]
        ] = None,
        flags: Flags = Flags.NO,
    ):

        buttons_edited = []
        row = []

        if isinstance(buttons, SillyButton):
            buttons_edited = [[buttons]]
        if isinstance(buttons, Sequence):
            for x in buttons:
                if isinstance(x, SillyButton):
                    buttons_edited.append(row)
                    row = []
                    buttons_edited.append([x])
                if isinstance(x, Sequence):
                    if row:
                        buttons_edited.append(row)
                    row = []
                    for y in x:
                        row.append(y)

        if row:
            buttons_edited.append(row)

        self._name = name
        self._text = text
        self._buttons = buttons_edited
        self._privileged = privileged

        self._flags = flags

        async def format_default(manager: SillyManager, event: SillyEvent):
            return ()

        self._get_format_args = get_format_args if get_format_args else format_default
