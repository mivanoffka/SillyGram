from typing import Dict, List, Optional
from .text import SillyText
import json
from config import PATH
from pathlib import Path


class SillyTextStorage:
    _storage: Dict[str, SillyText] = {}

    def new(self, key: str, text: str | Dict[str | List[str], str]) -> SillyText:
        if key in self._storage:
            raise KeyError(f'Key {key} already exists')

        silly_text = SillyText(text)
        self._storage[key] = silly_text

        return silly_text

    def __getitem__(self, item):
        return self._storage[item]

    def _to_dictionary(self) -> Dict[str, Dict[str | List[str], str]]:
        dictionary = {}

        for key in self._storage.keys():
            dictionary[key] = self._storage[key].dictionary

        return dictionary

    def _from_dictionary(self, dictionary: Dict[str, Dict[str | List[str], str]]):
        storage = {}
        for key in dictionary.keys():
            storage[key] = SillyText(dictionary[key])

        self._storage = storage

    def save_to_json(self, file_name: str):
        file_name = SillyTextStorage._validate_file_name(file_name)
        with open(PATH / file_name, 'w') as json_file:
            json.dump(self._to_dictionary, json_file, ensure_ascii=False, indent=4)

    def load_from_json(self, file_name: str):
        file_name = SillyTextStorage._validate_file_name(file_name)
        with open(PATH / file_name, "r") as json_file:
            data = json.load(json_file)
            self._from_dictionary(data)

    @staticmethod
    def _validate_file_name(file_name: str):
        return file_name if Path(file_name).is_absolute() else PATH / file_name

    def __init__(self, file_name: Optional[str] = None):
        if file_name is None:
            return

        self.load_from_json(file_name)
        print(self._to_dictionary())
