from sillygram import (
    SillyPage,
    NavigationSillyButton,
    ActionSillyButton,
    SillyManager,
    SillyEvent,
    SILLY_HOME_PAGE_POINTER
)
from ..text import Text


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
)