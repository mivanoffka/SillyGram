from sillygram import SillyText

class TestSillyText:
    def test_no_format(self):
        text = SillyText("Hello, World!")
        text = text.format()

        assert text.localize() == "Hello, World!"
        assert text.localize("en") == "Hello, World!"
        assert text.localize("ru") == "Hello, World!"
        assert text.localize("uk") == "Hello, World!"

    def test_single_string(self):
        text = SillyText("Hello, {}!")
        text = text.format("World")

        assert text.localize() == "Hello, World!"
        assert text.localize("en") == "Hello, World!"
        assert text.localize("ru") == "Hello, World!"
        assert text.localize("uk") == "Hello, World!"

    def test_single_element_dict(self):
        text = SillyText({"en": "Hello, {}!"})
        text = text.format("World")

        assert text.localize() == "Hello, World!"
        assert text.localize("en") == "Hello, World!"
        assert text.localize("ru") == "Hello, World!"
        assert text.localize("uk") == "Hello, World!"

    def test_multiple_element_dict(self):
        text = SillyText({"en": "Hello, {}!", "ru": "Привет, {}!"})
        text = text.format("World")

        assert text.localize("en") == "Hello, World!"
        assert text.localize("ru") == "Привет, World!"
        assert text.localize("uk") == "Hello, World!"

    def test_listed_lang_codes(self):
        text = SillyText({"en": "Hello, {}!", ("ru", "ua"): "Привет, {}!"})
        text = text.format("World")

        assert text.localize("en") == "Hello, World!"
        assert text.localize("ru") == "Привет, World!"
        assert text.localize("ua") == "Привет, World!"

    def test_redundant_placeholders(self):
        text = SillyText("Hello, {}! My name is {}.")
        text = text.format("World")

        assert text.localize() == "Hello, World! My name is {}.".format(SillyText._undefined_content)

    def test_redundant_args(self):
        text = SillyText("Hello, {}!")
        text = text.format("World", "John")

        assert text.localize() == "Hello, World!"
