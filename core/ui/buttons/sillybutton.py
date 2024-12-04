from typing import Dict, Sequence, Any


class SillyButton:
    _text: str | Dict[str | Sequence[str], str]

    @property
    def text(self) -> str | Dict[str | Sequence[str], str]:
        return self._text

    def aiogramify(self, language_code: str) -> Any:
        raise NotImplementedError()

    def __init__(self, text: str | Dict[str | Sequence[str], str]):
        self._text = text
