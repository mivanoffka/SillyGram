from sillygram import (
    SillyPage,
    SillyNavigationButton,
    SillyActionButton,
    SillyManager,
    SillyEvent,
    SILLY_HOME_PAGE_POINTER,
)
from ...sillygram.data.registry.registry import SillyRegistry
from ..text import Text


async def _get_format_args(manager: SillyManager, event: SillyEvent):
    KEY_NAME = "format_page_visited_count"

    str_value = event.user.registry[KEY_NAME]
    if str_value is not SillyRegistry.NotFound:
        event.user.registry[KEY_NAME] = "1"
    else:
        event.user.registry[KEY_NAME] = str(int(str_value) + 1)

    current_value = event.user.registry[KEY_NAME] 
    return (event.user.nickname, current_value)


async def _on_more_info_clicked(manager: SillyManager, event: SillyEvent):
    await manager.show_popup(event.user, Text.FormatPage.MORE_INFO_TEXT)


format_page = SillyPage(
    name=Text.FormatPage.NAME,
    text=Text.FormatPage.TEXT,
    buttons=(
        (
            SillyNavigationButton(
                text=Text.BACK_BUTTON, page_name=SILLY_HOME_PAGE_POINTER
            ),
            SillyActionButton(
                text=Text.FormatPage.MORE_INFO_BUTTON_TEXT,
                on_click=_on_more_info_clicked,
            ),
        ),
    ),
    get_format_args=_get_format_args,
)
