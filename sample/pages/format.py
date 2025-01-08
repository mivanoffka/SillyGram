from sillygram import (
    SillyPage,
    NavigationSillyButton,
    ActionSillyButton,
    SillyManager,
    SillyEvent,
    SILLY_HOME_PAGE_POINTER
)
from ..text import Text

async def get_format_args(manager: SillyManager, event: SillyEvent):
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
            
        return (event.user.nickname, current_value)

async def _on_more_info_clicked(manager: SillyManager, event: SillyEvent):
    await manager.show_popup(event.user, Text.FormatPage.MORE_INFO_TEXT)

format_page = SillyPage(
    name=Text.FormatPage.NAME,
    text=Text.FormatPage.TEXT,
    buttons=(
        (
            NavigationSillyButton(text=Text.BACK_BUTTON, page_name=SILLY_HOME_PAGE_POINTER),
            ActionSillyButton(
                text=Text.FormatPage.MORE_INFO_BUTTON_TEXT, on_click=_on_more_info_clicked
            ),
        ),
    ),
    get_format_args=get_format_args,
)