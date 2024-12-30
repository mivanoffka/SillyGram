from sillygram import SillyText


class Text:
    class StartPage:
        TEXT = SillyText(
            {
                "en": "Welcome to Silly-Sample-Bot!\n\n<blockquote>This page is labeled as <i>START</i>. Users see it when they launch the bot first time. \n\nIt may be later accessed using <code>/start</code> command.</blockquote>",
            }
        )
        NEXT_BUTTON = SillyText({"en": "Next"})

    class HomePage:
        TEXT = SillyText(
            {
                "en": "Home sweet home!\n\n<blockquote>This is the HOME page. It is meant to be the main page of any bot. From there you can navigate to any other pages.\n\nIt may be accessed using <code>/home</code> command. \n\nMoreover, if anything goes wrong and a page crashes, users will be redirected here.</blockquote>",
            }
        )
        GOTO_MESSAGE_BUTTON_TEXT = SillyText({"en": "Messenging"})
        GOTO_INPUT_BUTTON_TEXT = SillyText({"en": "Input"})
        GOTO_DIALOG_BUTTON_TEXT = SillyText({"en": "Dialog"})

    class InputPage:
        NAME = "Input"
        TEXT = SillyText(
            {
                "en": "Here you can test input functions of SillyGram",
            }
        )
        TEXT_INPUT_BUTTON = SillyText({"en": "Text Input"})
        TEXT_INPUT_PROMPT = SillyText({"en": "Please, enter something"})
        TEXT_INPUT_RESULT_TEMPLATE = SillyText({"en": 'You entered:\n\n "{}"'})

    class MessagePage:
        NAME = "Message"
        TEXT = SillyText(
            {
                "en": "Here you can test message functions of SillyGram",
            }
        )
        PREFIX_MESSAGE_BUTTON_TEXT = SillyText({"en": "Prefix"})
        INFIX_MESSAGE_BUTTON_TEXT = SillyText({"en": "Infix"})
        POSTFIX_MESSAGE_BUTTON_TEXT = SillyText({"en": "Postfix"})
        MESSAGE_BUTTON_TEXT = SillyText({"en": "Message"})

        PREFIX_MESSAGE_TEXT = SillyText({"en": "That's a prefix message!"})
        INFIX_MESSAGE_TEXT = SillyText({"en": "That's an infix message!"})
        POSTFIX_MESSAGE_TEXT = SillyText({"en": "That's a postfix message!"})
        MESSAGE_TEXT = SillyText({"en": "That's a message!"})

    class DialogPage:
        NAME = "Dialog"
        TEXT = SillyText(
            {
                "en": "Here you can test dialog functions of SillyGram",
            }
        )

        YES_NO_DIALOG_BUTTON = SillyText({"en": "Yes/No"})
        YES_NO_DIALOG_TEXT = SillyText(
            {
                "en": "Yes or No?\n\n<blockquote>This is a standard SillyGram dialog with two options</blockquote>"
            }
        )
        YES_NO_DIALOG_RESULT_TEMPLATE = SillyText(
            {
                "en": "You have chosen '{}'\n\n<blockquote>The result is a boolean value.\n\nYes stands for True, No stands for False.</blockquote>"
            }
        )

        CUSTOM_DIALOG_BUTTON = SillyText({"en": "Custom"})
        CUSTOM_DIALOG_TEXT = SillyText({"en": "Choose an option"})
        CUSTOM_DIALOG_OPTIONS = (
            SillyText({"en": "Red"}),
            SillyText({"en": "Green"}),
            SillyText({"en": "Blue"}),
        )
        CUSTOM_DIALOG_RESULT_TEMPLATE = SillyText(
            {"en": "You have chosen '{}'"}
        )

    BACK_BUTTON = SillyText({"en": "Back"})
