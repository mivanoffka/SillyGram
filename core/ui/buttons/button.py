from typing import Dict, List, Sequence

from ..aiogramable import Aiogramable
# #from utility import SillyText


class Button(Aiogramable):
    _text: str | Dict[str | Sequence[str], str]

    @property
    def text(self) -> str | Dict[str | List[str], str]:
        return self._text

    def aiogramify(self, language_code) -> any:
        raise NotImplementedError()

    def __init__(self, text: str | Dict[str | Sequence[str], str]):
        self._text = text
