from typing import Dict, Optional, List
from langcodes import Language


class SillyText:
    _dictionary: Optional[Dict[str, str]] = None
    _default: Optional[str] = None

    def _get(self, language: str | int) -> str:
        if (self._dictionary is None
                or language is None
                or language == ""
                or language == 0):
            return self._default

        if not Language.get(language).is_valid():
            raise ValueError("Language code '{}' is invalid".format(language))

        language = str(Language.get(language))

        if language not in self._dictionary.keys():
            return self._default

        return self._dictionary[language]

    def __getitem__(self, item: str | int) -> str:
        return self._get(item)

    def __str__(self):
        return self._default

    @property
    def dictionary(self) -> Dict[str, str]:
        return self._dictionary

    def __init__(self, text: str | Dict[str | List[str], str]):
        if isinstance(text, str):
            self._default = text
        elif isinstance(text, dict):
            dictionary = {}

            for key in text.keys():
                if isinstance(key, str):
                    lang = Language.get(key)
                    if not lang.is_valid():
                        raise ValueError("Language code '{}' is invalid".format(key))
                    dictionary[str(lang)] = text[key]
                elif isinstance(key, list):
                    for language_code in key:
                        lang = Language.get(language_code)
                        if not lang.is_valid():
                            raise ValueError("Language code '{}' is invalid".format(language_code))
                        dictionary[str(lang)] = text[key]

            self._dictionary = dictionary
            self._default = self._dictionary[tuple(key for key in self._dictionary.keys())[0]]

