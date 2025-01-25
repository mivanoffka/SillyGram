from ..text import Text
from sillygram import SillyPage, SillyNavigationButton


start_page = SillyPage(
    name="Start",
    text=Text.StartPage.TEXT,
    flags=SillyPage.Flags.START,
    buttons=[
        [SillyNavigationButton(text=Text.StartPage.NEXT_BUTTON, page_name="Home")]
    ],
)
