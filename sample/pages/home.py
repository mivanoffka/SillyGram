from ..text import Text
from sillygram import SillyPage, SillyNavigationButton


home_page = SillyPage(
    name="Home",
    text=Text.HomePage.TEXT,
    buttons=(
        (
            SillyNavigationButton(
                text=Text.HomePage.GOTO_INPUT_BUTTON_TEXT, page_name=Text.InputPage.NAME
            ),
            SillyNavigationButton(
                text=Text.HomePage.GOTO_MESSAGE_BUTTON_TEXT,
                page_name=Text.MessagePage.NAME,
            ),
        ),
        (
            SillyNavigationButton(
                text=Text.HomePage.GOTO_DIALOG_BUTTON_TEXT,
                page_name=Text.DialogPage.NAME,
            ),
            SillyNavigationButton(
                text=Text.HomePage.GOTO_FORMAT_BUTTON_TEXT,
                page_name=Text.FormatPage.NAME,
            ),
        )
    ),
    flags=SillyPage.Flags.HOME
)