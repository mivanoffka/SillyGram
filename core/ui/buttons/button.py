from typing import Dict, List, Sequence


class Button:
    _text: str | Dict[str | Sequence[str], str]

    @property
    def text(self) -> str | Dict[str | List[str], str]:
        return self._text

    def aiogramify(self, language_code) -> any:
        raise NotImplementedError()

    def __init__(self, text: str | Dict[str | Sequence[str], str]):
        self._text = text
