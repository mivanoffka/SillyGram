import pytest
from sillygram import SillyText

class TestSillyTextValidInit:
    def test_single_string(self):
        SillyText("Hello, World!")

    def test_single_element_dict(self):
        SillyText({"en": "Hello, World!"})

    def test_multiple_element_dict(self):
        SillyText({"en": "Hello, World!", "ru": "Привет, Мир!"})

    def test_listed_lang_codes(self):
        SillyText({"en": "Hello, World!", ("ru",): "Привет, Мир!"})

    def test_format(self):
        SillyText({"en": "Hello, {}!", "ru": "Привет, {}!"})

class TestSillyTextInvalidInit:
    def test_empty(self):
        with pytest.raises(TypeError):
            SillyText()  # type: ignore

    def test_invalid_type(self):
        with pytest.raises(TypeError):
            SillyText(42)  # type: ignore

    def test_invalid_dict_key(self):
        with pytest.raises(TypeError):
            SillyText({42: "Hello, World!"})  # type: ignore

    def test_invalid_dict_value(self):
        with pytest.raises(TypeError):
            SillyText({"en": 42})  # type: ignore

    def test_invalid_dict_value_list(self):
        with pytest.raises(TypeError):
            SillyText({"en": ["Hello, World!"]})  # type: ignore

    def test_invalid_dict_key_list(self):
        with pytest.raises(TypeError):
            SillyText({("en", 12): "Hello, World!"})  # type: ignore

    def test_format(self):
        with pytest.raises(ValueError):
            SillyText({"en": "Hello, {}!", "ru": "Привет, {} {}!"})

