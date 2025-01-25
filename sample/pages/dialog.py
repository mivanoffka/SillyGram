from ..text import Text
from sillygram import (
    SillyPage,
    SillyNavigationButton,
    SILLY_HOME_PAGE_POINTER,
    SillyManager,
    SillyEvent,
    SillyActionButton,
)


async def on_yes_no_button_clicked(manager: SillyManager, event: SillyEvent):
    answer = await manager.get_yes_no_answer(event.user, Text.DialogPage.YES_NO_DIALOG_TEXT)
    if answer is None:
        return
    await manager.show_popup(
        event.user, Text.DialogPage.YES_NO_DIALOG_RESULT_TEMPLATE.format(answer)
    )


async def on_custom_button_clicked(manager: SillyManager, event: SillyEvent):
    answer = await manager.show_dialog(
        event.user, Text.DialogPage.CUSTOM_DIALOG_TEXT, *Text.DialogPage.CUSTOM_DIALOG_OPTIONS, cancelable=True
    )
    if answer is not None:
        await manager.show_popup(
            event.user,
            Text.DialogPage.CUSTOM_DIALOG_RESULT_TEMPLATE.format(
                Text.DialogPage.CUSTOM_DIALOG_OPTIONS[answer]
            ),
        )


dialog_page = SillyPage(
    name=Text.DialogPage.NAME,
    text=Text.DialogPage.TEXT,
    buttons=[
        [
            SillyNavigationButton(Text.BACK_BUTTON, SILLY_HOME_PAGE_POINTER),
            SillyActionButton(
                Text.DialogPage.CUSTOM_DIALOG_BUTTON, on_custom_button_clicked
            ),
            SillyActionButton(
                Text.DialogPage.YES_NO_DIALOG_BUTTON, on_yes_no_button_clicked
            ),
        ]
    ],
)
