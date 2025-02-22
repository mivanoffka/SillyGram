from typing import Optional

from ...manager import SillyManager
from ...events import SillyEvent
from ...user import SillyUser

from ...ui import SillyPage, SillyActionButton, SillyNavigationButton

from ...data import SillyDefaults
from ..common import get_user

from .broadcaster import broadcaster


@SillyManager.privileged()
async def _on_send_message_button_clicked(manager: SillyManager, event: SillyEvent):
    user_to_text: Optional[SillyUser]
    user_to_text = await get_user(manager, event)
    if not user_to_text:
        return

    message_text = await manager.get_input(
        event.user,
        SillyDefaults.Controls.CommunicationPage.PERSONAL_MESSAGE_TEXT.format(
            user_to_text.nickname_or_id
        ),
    )
    if not message_text:
        return

    combined_text = (
        SillyDefaults.Controls.CommunicationPage.MESSAGE_RECEIVED_TEMPLATE.format(
            manager._data.settings.labels.message_recieved, message_text
        )
    )

    await manager.show_notice(user_to_text, combined_text)
    await manager.show_popup(
        event.user,
        SillyDefaults.Controls.CommunicationPage.MESSAGE_DELIVERED_TEXT.format(
            user_to_text.nickname_or_id
        ),
    )


@SillyManager.privileged()
async def _on_broadcast_button_clicked(manager: SillyManager, event: SillyEvent):
    if broadcaster.is_busy:
        await manager.show_page(
            event.user, SillyDefaults.Controls.BroadcastStatusPage.NAME
        )
    else:
        message_text = await manager.get_input(
            event.user,
            SillyDefaults.Controls.CommunicationPage.BROADCAST_MESSAGE_TEXT,
        )
        if not message_text:
            return

        if await broadcaster.try_show_broadcast_notice(manager, message_text):
            await manager.show_popup(
                event.user,
                SillyDefaults.Controls.CommunicationPage.BROADCAST_SUCCESS_TEXT,
            )


communication_page = SillyPage(
    SillyDefaults.Controls.CommunicationPage.NAME,
    SillyDefaults.Controls.CommunicationPage.TEXT,
    buttons=(
        (
            SillyActionButton(
                SillyDefaults.Controls.CommunicationPage.SEND_MESSAGE_BUTTON_TEXT,
                _on_send_message_button_clicked,
            ),
            SillyActionButton(
                SillyDefaults.Controls.CommunicationPage.BROADCAST_BUTTON_TEXT,
                _on_broadcast_button_clicked,
            ),
        ),
        (
            SillyNavigationButton(
                SillyDefaults.Controls.BACK_BUTTON_TEXT,
                SillyDefaults.Names.Pages.CONTROLS,
            ),
        ),
    ),
)
