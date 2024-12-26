from sillygram import SillyText

class TestSillyTextLocalize:
    def test_single_string(self):
        text = SillyText("Hello, World!")

        assert text.localize() == "Hello, World!"
        assert text.localize("en") == "Hello, World!"
        assert text.localize("ru") == "Hello, World!"
        assert text.localize("uk") == "Hello, World!"

    def test_single_element_dict(self):
        text = SillyText({"en": "Hello, World!"})

        assert text.localize() == "Hello, World!"
        assert text.localize("en") == "Hello, World!"
        assert text.localize("ru") == "Hello, World!"
        assert text.localize("uk") == "Hello, World!"

    def test_multiple_element_dict(self):
        text = SillyText({"en": "Hello, World!", "ru": "Привет, Мир!"})
        assert text.localize("en") == "Hello, World!"
        assert text.localize("ru") == "Привет, Мир!"
        assert text.localize("uk") == "Hello, World!"

    def test_listed_lang_codes(self):
        text = SillyText({"en": "Hello, World!", ("ru", "ua"): "Привет, Мир!"})
        assert text.localize("en") == "Hello, World!"
        assert text.localize("ru") == "Привет, Мир!"
        assert text.localize("ua") == "Привет, Мир!"
