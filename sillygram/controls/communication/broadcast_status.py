from ...manager import SillyManager
from ...events import SillyEvent

from ...ui import SillyPage, SillyActionButton, SillyNavigationButton

from ...data import SillyDefaults

from .broadcaster import broadcaster


async def _on_refresh_button_clicked(manager: SillyManager, event: SillyEvent):
    await manager.show_page(
        event.user, SillyDefaults.Controls.BroadcastStatusPage.NAME
    )


async def _get_format_args(manager: SillyManager, event: SillyEvent):
    return (
        broadcaster.processed_users_count,
        broadcaster.total_users_count,
        round(broadcaster.progress * 100) if broadcaster.progress is not None else "?",
    )

async def _on_stop_broadcast_button_clicked(manager: SillyManager, event: SillyEvent):
    if await manager.get_yes_no_answer(event.user, SillyDefaults.Controls.BroadcastStatusPage.STOP_CONFIRMATION_TEXT):
        await broadcaster.stop()
        await manager.show_page(event.user,  SillyDefaults.Names.Pages.CONTROLS)
        await manager.show_notice(event.user, SillyDefaults.Controls.BroadcastStatusPage.BROADCAST_STOPPED_TEXT)


broadcast_status_page = SillyPage(
    SillyDefaults.Controls.BroadcastStatusPage.NAME,
    SillyDefaults.Controls.BroadcastStatusPage.TEXT,
    buttons=(
        (
            SillyActionButton(
                SillyDefaults.Controls.BroadcastStatusPage.REFRESH_BUTTON_TEXT,
                _on_refresh_button_clicked,
            ),
        ),
        (
            SillyNavigationButton(
                SillyDefaults.Controls.BACK_BUTTON_TEXT,
                 SillyDefaults.Names.Pages.CONTROLS,
            ),
            SillyActionButton(
                SillyDefaults.Controls.BroadcastStatusPage.STOP_BROADCAST_BUTTON_TEXT,
                _on_stop_broadcast_button_clicked,
            ),
        ),
    ),
    get_format_args=_get_format_args,
)
