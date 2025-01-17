from ..text import Text
from sillygram import SillyPage, NavigationSillyButton


start_page = SillyPage(
    name="Start",
    text=Text.StartPage.TEXT,
    flags=SillyPage.Flags.START,
    buttons=[
        [NavigationSillyButton(text=Text.StartPage.NEXT_BUTTON, page_name="Home")]
    ],
)
