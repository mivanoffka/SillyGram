from typing import Dict
from collections.abc import Sequence


def localize(text: str | Dict[str | Sequence[str], str], language_code: str) -> str:
    if isinstance(text, str):
        return text

    for key in text.keys():
        if isinstance(key, str):
            if language_code.lower() == key.lower():
                return text[key]
        if isinstance(key, Sequence):
            for subkey in key:
                if language_code.lower() == subkey.lower():
                    return text[key]

    return text[tuple(text.keys())[0]]
