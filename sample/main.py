from sillygram import SillyBot, SillySettings
from .pages import home_page, start_page, input_page, message_page, dialog_page, format_page

from .config import TOKEN, LOG_TO_CONSOLE

if __name__ == "__main__":
    pages = (home_page, start_page, input_page, message_page, dialog_page, format_page)

    if TOKEN:
        silly_bot: SillyBot = SillyBot(
            TOKEN,
            pages=pages,
            settings=SillySettings(log_to_console=LOG_TO_CONSOLE),
        )

        silly_bot.launch()
