class SillyRegistryKey:
    _name: str
    _user_id: int

    @property
    def name(self):
        return self._name

    @property
    def user_id(self):
        return self._user_id

    def __init__(self, name: str, user_id: int):
        self._name = name
        self._user_id = user_id
