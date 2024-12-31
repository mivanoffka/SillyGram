from ..text import Text
from sillygram import SillyPage, NavigationSillyButton, ActionSillyButton, SillyEvent, SillyManager


async def on_format_button_clicked(manager: SillyManager, event: SillyEvent):
    KEY_NAME = "format_page_visited_count"
    
    if KEY_NAME not in manager.registry.disk.get_keys():
        manager.registry.disk.establish_key(KEY_NAME, "0")
    if KEY_NAME in manager.registry.disk.get_keys():
        str_value = manager.registry.disk.get_value(KEY_NAME)
        if str_value:
            manager.registry.disk.set_value(KEY_NAME, str(int(str_value) + 1))
        else:
            manager.registry.disk.set_value(KEY_NAME, "1")

    current_value = manager.registry.disk.get_value(KEY_NAME)
    if not current_value:
        current_value = "1"

    await manager.show_page(event.user, Text.FormatPage.NAME, args=(event.user.nickname, current_value))
    

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
        ),
        (
            NavigationSillyButton(
                text=Text.HomePage.GOTO_DIALOG_BUTTON_TEXT,
                page_name=Text.DialogPage.NAME,
            ),
            ActionSillyButton(
                text=Text.HomePage.GOTO_FORMAT_BUTTON_TEXT,
                on_click=on_format_button_clicked,
            ),
        )
    ),
    is_home=True,
)