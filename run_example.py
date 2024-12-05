from core import SillyBot, SillySettings, SillyManager
from example.pages import home_page, start_page, widgets_page
import os

from core.activities import SillyDateTimeActivity
from datetime import time, timedelta


async def increment(manager: SillyManager):
    manager.registry.session["key"] = (int(manager.registry.session["key"]) + 1)
    print(manager.registry.session["key"])


async def on_start(manager: SillyManager):
    manager.registry.session.establish_key("key", "0")


TOKEN = os.environ.get("TOKEN")
LOG_TO_CONSOLE = True

pages = (home_page, start_page, widgets_page)
activities = (SillyDateTimeActivity(activity=increment, times=time(hour=21, minute=20), max_time_delta=timedelta(hours=1)),)

silly_bot: SillyBot = SillyBot(TOKEN, pages=pages, regular_activities=activities,
                               settings=SillySettings(log_to_console=LOG_TO_CONSOLE),
                               startup_activity=on_start)

if __name__ == '__main__':
    silly_bot.launch()
