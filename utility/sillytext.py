from typing import Dict, Sequence


class SillyText:
    _text: str | Dict[str | Sequence[str], str]

    def format(self, *args, **kwargs):
        if isinstance(self._text, str):
            SillyText(self._text.format(*args, **kwargs))

        if isinstance(self._text, dict):
            text = {}

            for key in self._text.keys():
                if isinstance(key, str) or isinstance(key, Sequence):
                    text[key] = self._text[key].format(*args, **kwargs)

            return SillyText(text)

        return SillyText(self._text)

    def localize(self, language_code: str) -> str:
        if isinstance(self._text, str):
            return self._text

        for key in self._text.keys():
            if isinstance(key, str):
                if language_code.lower() == key.lower():
                    return self._text[key]
            if isinstance(key, Sequence):
                for subkey in key:
                    if language_code.lower() == subkey.lower():
                        return self._text[key]

        return self._text[tuple(self._text.keys())[0]]

    def __init__(self, text: str | Dict[str | Sequence[str], str]):
        self._text = text
