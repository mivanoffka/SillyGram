from sillygram import privilege
from ..ui import SillyActionButton, SillyPage, SillyNavigationButton
from ..data import SillyDefaults
from ..manager import SillyManager
from ..text import SillyText
from ..events import SillyEvent
from .common import get_user


@SillyManager.privileged()
async def _not_implemented(manager: SillyManager, event: SillyEvent):
    await manager.show_popup(event.user, SillyDefaults.Controls.NOT_IMPLEMENTED_TEXT)


@SillyManager.privileged()
async def _on_stats_button_clicked(manager: SillyManager, event: SillyEvent):
    await manager.show_popup(event.user, manager.stats)


@SillyManager.privileged()
async def _on_privileges_button_clicked(manager: SillyManager, event: SillyEvent):
    user_to_check = await get_user(manager, event)
    if not user_to_check:
        return

    privilege_name = user_to_check.privilege_name
    text_to_show = SillyDefaults.Controls.NEGATIVE_PRIVILEGE_INFO.format(
        user_to_check.nickname_or_id
    )
    if privilege_name:
        text_to_show = SillyDefaults.Controls.POSITIVE_PRIVILEGE_INFO.format(
            user_to_check.nickname_or_id, privilege_name
        )

    if not await manager.get_yes_no_answer(event.user, text_to_show):
        return

    privilege_options = (
        *[SillyText(text) for text in manager.privileges_names],
        SillyDefaults.Controls.DEFAULT_PRIVILEGE,
    )

    privilege_id = await manager.show_dialog(
        event.user,
        SillyDefaults.Controls.PRIVEGELE_PROMPT.format(user_to_check.nickname_or_id),
        *privilege_options
    )

    if privilege_id is not None:
        text = SillyDefaults.Controls.PRIVILEGE_NEGATIVE_SETTING_SUCCESS.format(
            user_to_check.nickname_or_id
        )
        if privilege_id in range(len(manager.privileges_names)):
            text = SillyDefaults.Controls.PRIVILEGE_POSITIVE_SETTING_SUCCESS.format(
                user_to_check.nickname_or_id, manager.privileges_names[privilege_id]
            )
            manager.set_privilege(user_to_check, manager.privileges_names[privilege_id])
        else:
            manager.set_privilege(user_to_check, None)

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
                SillyDefaults.Controls.PRIVILEGES_BUTTON_TEXT,
                _on_privileges_button_clicked,
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
