import logging
from typing import Dict, List, Optional, Sequence


class SillyText:
    _text: str | Dict[str | Sequence[str], str]
    _undefined_content: str = "?"

    def _fix_args_count(self, args: List[str], text_to_format: str) -> List[str]:
        placeholders_count = text_to_format.count("{}")

        if len(args) > placeholders_count:
            args = args[:placeholders_count]
            logging.warning(
                f"Too many arguments passed to '{text_to_format}'. Only {args} will be used."
            )

        elif len(args) < placeholders_count:
            for _ in range(placeholders_count - len(args)):
                args.append(self._undefined_content)
            logging.warning(f"Not enough arguments passed to '{text_to_format}'. Missing will be filled with '{self._undefined_content}'.")

        return args

    def format(self, *args: object) -> "SillyText":
        if args is None or len(args) == 0:
            return SillyText(self._text)

        _args: List[str] = [str(arg) for arg in args]

        if isinstance(self._text, str):
            return SillyText(self._text.format(*self._fix_args_count(_args, self._text)))

        if isinstance(self._text, dict):
            text = {}

            for key in self._text.keys():
                if isinstance(key, str) or isinstance(key, Sequence):
                    text[key] = self._text[key].format(*self._fix_args_count(_args, self._text[key]))

            return SillyText(text)

        return SillyText(self._text)

    def localize(self, language_code: Optional[str] = None) -> str:
        if isinstance(self._text, str):
            return self._text

        if language_code is not None:
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
        logging.warning(
            "Do not pass SillyText when a casual string required. SillyText must be localized first."
        )
        if isinstance(self._text, str):
            return self._text

        return self._text[tuple(self._text.keys())[0]]

    def __init__(self, text: str | Dict[str | Sequence[str], str]):
        if not isinstance(text, str) and not isinstance(text, dict):
            raise TypeError(
                f"Expected 'text' to be str or Dict, got {type(text).__name__}"
            )

        formats_count = []
        if isinstance(text, dict):
            for key, value in text.items():
                if not isinstance(key, (str, Sequence)):
                    raise TypeError(
                        f"Dict key must be str or Sequence[str], got {type(key).__name__}"
                    )
                if isinstance(key, Sequence) and not all(
                    isinstance(item, str) for item in key
                ):
                    raise TypeError("All items in key sequence must be str")
                if not isinstance(value, str):
                    raise TypeError(
                        f"Dict value must be str, got {type(value).__name__}"
                    )

                formats_count.append(value.count("{}"))

        for format_count in formats_count:
            if format_count != formats_count[0]:
                raise ValueError(
                    "All values in dict must have the same amount of format placeholders"
                )

        self._text = text
