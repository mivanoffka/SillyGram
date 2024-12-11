import logging
from typing import Dict, Sequence


class SillyText:
    _text: str | Dict[str | Sequence[str], str]

    def format(self, *args: object) -> "SillyText":
        if args is None or len(args) == 0:
            return SillyText(self._text)

        args = tuple(str(arg) for arg in args)

        if isinstance(self._text, str):
           return SillyText(self._text.format(*args))

        if isinstance(self._text, dict):
            text = {}

            for key in self._text.keys():
                if isinstance(key, str) or isinstance(key, Sequence):
                    text[key] = self._text[key].format(*args)

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

    def __str__(self):
        logging.warning("Do not pass SillyText when a casual string required. SillyText must be localized first.")
        if isinstance(self._text, str):
           return self._text

        return self._text[tuple(self._text.keys())[0]]

    def __init__(self, text: str | Dict[str | Sequence[str], str]):
        self._text = text
