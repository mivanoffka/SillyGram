from typing import Dict, List

from ..aiogramable import Aiogramable
from utility import SillyText


class Button(Aiogramable):
    _text: SillyText

    @property
    def text(self) -> SillyText:
        return self._text

    def aiogramify(self, language_code) -> any:
        raise NotImplementedError()

    def __init__(self, text: SillyText):
        self._text = text
