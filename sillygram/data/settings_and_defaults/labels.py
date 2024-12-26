from typing import Optional
from ...text import SillyText


class SillyLabels:
    _go_back = SillyText("Go back")
    _close = SillyText("Close")
    _cancel = SillyText("Cancel")
    _go_on = SillyText("Go on")
    _yes = SillyText("Yes")
    _no = SillyText("No")
    _emoji_separator = SillyText("✨")
    _admin_only = SillyText("Access denied.")
    _id_not_recognized = SillyText("Unable to recognize ID.")
    _promotion_success = SillyText("User {} was successfully promoted.")
    _demotion_success = SillyText("User {} was successfully demoted.")

    @property
    def go_back(self):
        return self._go_back

    @property
    def close(self):
        return self._close

    @property
    def cancel(self):
        return self._cancel

    @property
    def go_on(self):
        return self._go_on

    @property
    def yes(self):
        return self._yes

    @property
    def no(self):
        return self._no

    @property
    def emoji_separator(self):
        return self._emoji_separator

    @property
    def admin_only(self):
        return self._admin_only

    def __init__(
        self,
        go_back: Optional[SillyText] = None,
        close: Optional[SillyText] = None,
        go_on: Optional[SillyText] = None,
        cancel: Optional[SillyText] = None,
        yes: Optional[SillyText] = None,
        no: Optional[SillyText] = None,
        emoji_separator: Optional[SillyText] = None,
        admin_only: Optional[SillyText] = None,
    ):
        self._go_back = go_back if go_back else self._go_back
        self._close = close if close else self._close
        self._cancel = cancel if cancel else self._cancel
        self._yes = yes if yes else self._yes
        self._no = no if no else self._no
        self._emoji_separator = (
            emoji_separator if emoji_separator else self._emoji_separator
        )
        self._go_on = go_on if go_on else self._go_on
        self._cancel = admin_only if admin_only else self._cancel
