from ..text import Text
from sillygram import SillyPage, NavigationSillyButton


home_page = SillyPage(
    name="Home",
    text=Text.HomePage.TEXT,
    buttons=(
        (
            NavigationSillyButton(
                text=Text.HomePage.GOTO_INPUT_BUTTON_TEXT, page_name=Text.InputPage.NAME
            ),
            NavigationSillyButton(
                text=Text.HomePage.GOTO_MESSAGE_BUTTON_TEXT,
                page_name=Text.MessagePage.NAME,
            ),
            NavigationSillyButton(
                text=Text.HomePage.GOTO_DIALOG_BUTTON_TEXT,
                page_name=Text.DialogPage.NAME,
            )
        ),
    ),
    is_home=True,
)