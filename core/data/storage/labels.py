from typing import Optional


class SillyLabels:
    _go_back: str = "Go back"
    _close: str = "Close"
    _cancel: str = "Cancel"
    _go_on: str = "Go on"
    _yes: str = "Yes"
    _no: str = "No"
    _emoji_separator: str = "✨"

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
    def emoji_separator(self):
        return self._emoji_separator

    def __init__(self,
                 go_back: Optional[str] = None,
                 close: Optional[str] = None,
                 go_on: Optional[str] = None,
                 cancel: Optional[str] = None,
                 yes: Optional[str] = None,
                 no: Optional[str] = None,
                 emoji_separator: Optional[str] = None):
        self._go_back: str = go_back if go_back else self._go_back
        self._close: str = close if close else self._close
        self._cancel: str = cancel if cancel else self._cancel
        self._yes: str = yes if yes else self._yes
        self._no: str = no if no else self._no
        self._emoji_separator: str = emoji_separator if emoji_separator else self._emoji_separator
        self._go_on: str = go_on if go_on else self._go_on
