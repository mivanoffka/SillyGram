from typing import Any

from ...utility import SillyText


class SillyButton:
    _text: SillyText

    @property
    def text(self) -> SillyText:
        return self._text

    def aiogramify(self, language_code: str) -> Any:
        raise NotImplementedError()

    def __init__(self, text: SillyText):
        self._text = text
