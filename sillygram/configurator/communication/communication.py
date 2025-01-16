from typing import Optional

from ...manager import SillyManager
from ...events import SillyEvent
from ...user import SillyUser

from ...ui import SillyPage, ActionSillyButton, NavigationSillyButton

from ...data import SillyDefaults
from ..common import get_user

from .broadcaster import broadcaster


@SillyManager.priveleged()
async def _on_send_message_button_clicked(manager: SillyManager, event: SillyEvent):
    user_to_text: Optional[SillyUser]
    user_to_text = await get_user(manager, event)
    if not user_to_text:
        return

    message_text = await manager.get_input(
        event.user,
        SillyDefaults.Configurator.CommunicationPage.PERSONAL_MESSAGE_TEXT.format(
            user_to_text.nickname_or_id
        ),
    )
    if not message_text:
        return

    combined_text = (
        SillyDefaults.Configurator.CommunicationPage.MESSAGE_RECEIVED_TEMPLATE.format(
            manager._data.settings.labels.message_recieved, message_text
        )
    )

    await manager.show_notice(user_to_text, combined_text)
    await manager.show_popup(
        event.user,
        SillyDefaults.Configurator.CommunicationPage.MESSAGE_DELIVERED_TEXT.format(
            user_to_text.nickname_or_id
        ),
    )


@SillyManager.priveleged()
async def _on_broadcast_button_clicked(manager: SillyManager, event: SillyEvent):
    if broadcaster.is_busy:
        await manager.show_page(
            event.user, SillyDefaults.Configurator.BroadcastStatusPage.NAME
        )
    else:
        message_text = await manager.get_input(
            event.user,
            SillyDefaults.Configurator.CommunicationPage.BROADCAST_MESSAGE_TEXT,
        )
        if not message_text:
            return

        if await broadcaster.try_show_broadcast_notice(manager, message_text):
            await manager.show_popup(event.user, SillyDefaults.Configurator.CommunicationPage.BROADCAST_SUCCESS_TEXT)


communication_page = SillyPage(
    SillyDefaults.Configurator.CommunicationPage.NAME,
    SillyDefaults.Configurator.CommunicationPage.TEXT,
    buttons=(
        (
            ActionSillyButton(
                SillyDefaults.Configurator.CommunicationPage.SEND_MESSAGE_BUTTON_TEXT,
                _on_send_message_button_clicked,
            ),
            ActionSillyButton(
                SillyDefaults.Configurator.CommunicationPage.BROADCAST_BUTTON_TEXT,
                _on_broadcast_button_clicked,
            ),
        ),
        (
            NavigationSillyButton(
                SillyDefaults.Configurator.BACK_BUTTON_TEXT,
                SillyDefaults.Names.CONFIGURE_PAGE,
            ),
        ),
    ),
)
