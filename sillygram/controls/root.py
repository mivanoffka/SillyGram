from sillygram import privelege
from ..ui import SillyActionButton, SillyPage, SillyNavigationButton
from ..data import SillyDefaults
from ..manager import SillyManager
from ..text import SillyText
from ..events import SillyEvent
from .common import get_user


@SillyManager.priveleged()
async def _not_implemented(manager: SillyManager, event: SillyEvent):
    await manager.show_popup(event.user, SillyDefaults.Controls.NOT_IMPLEMENTED_TEXT)


@SillyManager.priveleged()
async def _on_stats_button_clicked(manager: SillyManager, event: SillyEvent):
    await manager.show_popup(event.user, manager.stats)


@SillyManager.priveleged()
async def _on_priveleges_button_clicked(manager: SillyManager, event: SillyEvent):
    user_to_check = await get_user(manager, event)
    if not user_to_check:
        return

    privelege_name = user_to_check.privelege_name
    text_to_show = SillyDefaults.Controls.NEGATIVE_PRIVELEGE_INFO.format(
        user_to_check.nickname_or_id
    )
    if privelege_name:
        text_to_show = SillyDefaults.Controls.POSITIVE_PRIVELEGE_INFO.format(
            user_to_check.nickname_or_id, privelege_name
        )

    if not await manager.get_yes_no_answer(event.user, text_to_show):
        return

    privelege_options = (
        *[SillyText(text) for text in manager.priveleges_names],
        SillyDefaults.Controls.DEFAULT_PRIVELEGE,
    )

    privelege_id = await manager.show_dialog(
        event.user,
        SillyDefaults.Controls.PRIVEGELE_PROMPT.format(user_to_check.nickname_or_id),
        *privelege_options
    )

    if privelege_id is not None:
        text = SillyDefaults.Controls.PRIVELEGE_NEGATIVE_SETTING_SUCCESS.format(
            user_to_check.nickname_or_id
        )
        if privelege_id in range(len(manager.priveleges_names)):
            text = SillyDefaults.Controls.PRIVELEGE_POSITIVE_SETTING_SUCCESS.format(
                user_to_check.nickname_or_id, manager.priveleges_names[privelege_id]
            )
            manager.set_privelege(user_to_check, manager.priveleges_names[privelege_id])
        else:
            manager.set_privelege(user_to_check, None)

        await manager.show_popup(event.user, text)


root_controls_page = SillyPage(
    name=SillyDefaults.Names.Pages.CONTROLS,
    text=SillyDefaults.Controls.ROOT_PAGE_TEXT,
    buttons=(
        (
            SillyNavigationButton(
                SillyDefaults.Controls.COMMUNICATION_BUTTON_TEXT,
                SillyDefaults.Controls.CommunicationPage.NAME,
            ),
        ),
        (
            SillyActionButton(
                SillyDefaults.Controls.PRIVELEGES_BUTTON_TEXT,
                _on_priveleges_button_clicked,
            ),
            SillyActionButton(
                SillyDefaults.Controls.STATS_BUTTON_TEXT, _on_stats_button_clicked
            ),
            SillyNavigationButton(
                SillyDefaults.Controls.BANNED_BUTTON_TEXT,
                SillyDefaults.Controls.BannedPage.NAME,
            ),
        ),
        (
            SillyNavigationButton(
                SillyDefaults.Controls.HOME_BUTTON_TEXT,
                SillyDefaults.Names.Pages.HOME,
            ),
            SillyNavigationButton(
                SillyDefaults.Controls.MORE_BUTTON_TEXT,
                SillyDefaults.Names.Pages.CUSTOM_CONTROLS,
                not_found_message=SillyDefaults.Controls.ADDITIONAL_CONTROLS_PAGE_TEMPLATE_TEXT,
            ),
        ),
    ),
)
