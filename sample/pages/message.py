from sillygram import (
    SillyPage,
    SillyNavigationButton,
    SillyActionButton,
    SillyManager,
    SillyEvent,
    SILLY_HOME_PAGE_POINTER,
)
from ..text import Text


async def on_banner_button_clicked(manager: SillyManager, event: SillyEvent):
    await manager.show_banner(event.user, Text.MessagePage.BANNER_MESSAGE_TEXT)


async def on_notice_button_clicked(manager: SillyManager, event: SillyEvent):
    await manager.show_notice(event.user, Text.MessagePage.NOTICE_MESSAGE_TEXT)


async def on_popup_button_clicked(manager: SillyManager, event: SillyEvent):
    await manager.show_popup(event.user, Text.MessagePage.POPUP_MESSAGE_TEXT)


message_page = SillyPage(
    name=Text.MessagePage.NAME,
    text=Text.MessagePage.TEXT,
    buttons=(
        (
            SillyActionButton(
                Text.MessagePage.NOTICE_MESSAGE_BUTTON_TEXT, on_notice_button_clicked
            ),  
            SillyActionButton(
                Text.MessagePage.POPUP_MESSAGE_BUTTON_TEXT, on_popup_button_clicked
            ),
            SillyActionButton(
                Text.MessagePage.BANNER_MESSAGE_BUTTON_TEXT, on_banner_button_clicked
            ),
        ),
        (
            SillyNavigationButton(Text.BACK_BUTTON, page_name=SILLY_HOME_PAGE_POINTER),
        ),
    ),
)
