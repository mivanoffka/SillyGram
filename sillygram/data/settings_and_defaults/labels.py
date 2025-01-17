from typing import Optional
from ...text import SillyText


class SillyLabels:
    _go_back = SillyText("Go back")
    _close = SillyText("Close")
    _cancel = SillyText("Cancel")
    _go_on = SillyText("Go on")
    _yes = SillyText("Yes")
    _no = SillyText("No")
    _access_denied = SillyText("Access denied.")
    _emoji_separator = SillyText("✨")

    _id_not_recognized = SillyText("Unable to recognize ID.")
    _promotion_success = SillyText("User {} was successfully promoted.")
    _demotion_success = SillyText("User {} was successfully demoted.")
    _error = SillyText("An error has occurred.\n<blockquote>{}</blockquote>")
    _try_again = SillyText("Please, try again.")
    _message_received = SillyText("You have got a message!")
    _page_not_found = SillyText("Page not found.")

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
    def access_denied(self):
        return self._access_denied

    @property
    def error(self):
        return self._error

    @property
    def try_again(self):
        return self._try_again
    
    @property
    def message_recieved(self):
        return self._message_received

    @property
    def page_not_found(self):
        return self._page_not_found

    def __init__(
        self,
        go_back: Optional[SillyText] = None,
        close: Optional[SillyText] = None,
        go_on: Optional[SillyText] = None,
        cancel: Optional[SillyText] = None,
        yes: Optional[SillyText] = None,
        no: Optional[SillyText] = None,
        emoji_separator: Optional[SillyText] = None,
        access_denied: Optional[SillyText] = None,
        error: Optional[SillyText] = None,
        try_again: Optional[Optional[SillyText]] = None,
        message_recieved: Optional[SillyText] = None,
        page_not_found: Optional[SillyText] = None,
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
        self._access_denied = access_denied if access_denied else self._access_denied
        self._error = error if error else self._error
        self._try_again = try_again if try_again else self._try_again
        self._message_received = message_recieved if message_recieved else self._message_received
        self._page_not_found = page_not_found if page_not_found else self._page_not_found
