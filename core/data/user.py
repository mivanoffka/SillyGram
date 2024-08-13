class SillyUser:

    @property
    def id(self) -> int:
        return self._id

    @property
    def nickname(self) -> str:
        return self._nickname

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def language_code(self) -> str:
        return self._language_code

    def __init__(self, id, nickname, first_name, last_name, language_code) -> None:
        self._id = id
        self._nickname = nickname
        self._first_name = first_name
        self._last_name = last_name
        self._language_code = language_code
