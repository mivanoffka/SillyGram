from sillygram import (
    SillyPage,
    NavigationSillyButton,
    ActionSillyButton,
    SillyManager,
    SillyEvent,
    SILLY_HOME_PAGE_POINTER
)
from ..text import Text


async def on_input_button_clicked(manager: SillyManager, event: SillyEvent):
    text = await manager.get_input(event.user, Text.InputPage.TEXT_INPUT_PROMPT)
    if text is not None:
        await manager.show_popup(
            event.user, Text.InputPage.TEXT_INPUT_RESULT_TEMPLATE.format(text)
        )


input_page = SillyPage(
    name=Text.InputPage.NAME,
    text=Text.InputPage.TEXT,
    buttons=(
        (
            NavigationSillyButton(text=Text.BACK_BUTTON, page_name=SILLY_HOME_PAGE_POINTER),
            ActionSillyButton(
                text=Text.InputPage.TEXT_INPUT_BUTTON, on_click=on_input_button_clicked
            ),
        ),
    ),
)
