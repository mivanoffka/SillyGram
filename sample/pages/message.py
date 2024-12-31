from sillygram import (
    SillyPage,
    NavigationSillyButton,
    ActionSillyButton,
    SillyManager,
    SillyEvent,
    SILLY_HOME_PAGE_POINTER,
)
from ..text import Text


async def on_prefix_button_clicked(manager: SillyManager, event: SillyEvent):
    await manager.show_banner(event.user, Text.MessagePage.PREFIX_MESSAGE_TEXT)


async def on_infix_button_clicked(manager: SillyManager, event: SillyEvent):
    await manager.show_interruption(event.user, Text.MessagePage.INFIX_MESSAGE_TEXT)


async def on_postfix_button_clicked(manager: SillyManager, event: SillyEvent):
    await manager.show_notification(event.user, Text.MessagePage.POSTFIX_MESSAGE_TEXT)


async def on_message_button_clicked(manager: SillyManager, event: SillyEvent):
    await manager.show_message(event.user, Text.MessagePage.MESSAGE_TEXT)


message_page = SillyPage(
    name=Text.MessagePage.NAME,
    text=Text.MessagePage.TEXT,
    buttons=(
        (
            ActionSillyButton(
                Text.MessagePage.PREFIX_MESSAGE_BUTTON_TEXT, on_prefix_button_clicked
            ),
            ActionSillyButton(
                Text.MessagePage.INFIX_MESSAGE_BUTTON_TEXT, on_infix_button_clicked
            ),
            ActionSillyButton(
                Text.MessagePage.POSTFIX_MESSAGE_BUTTON_TEXT, on_postfix_button_clicked
            ),
        ),
        (
            NavigationSillyButton(Text.BACK_BUTTON, page_name=SILLY_HOME_PAGE_POINTER),
            ActionSillyButton(
                Text.MessagePage.MESSAGE_BUTTON_TEXT, on_message_button_clicked
            ),
        ),
    ),
)
