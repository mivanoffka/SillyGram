from re import S
from sillygram import SillyBot, SillySettings, SillyLogger
from .pages import home_page, start_page, input_page, message_page, dialog_page, format_page

from .config import TOKEN

if __name__ == "__main__":
    pages = (home_page, start_page, input_page, message_page, dialog_page, format_page)

    if TOKEN:
        silly_bot: SillyBot = SillyBot(
            TOKEN,
            pages=pages,
        )

        silly_bot.launch()
