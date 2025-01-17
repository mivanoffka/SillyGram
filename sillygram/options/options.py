from sillygram import privelege
from ..ui import ActionSillyButton, SillyPage, NavigationSillyButton
from ..data import SillyDefaults
from ..manager import SillyManager
from ..text import SillyText
from ..events import SillyEvent
from .common import get_user


@SillyManager.priveleged()
async def _not_implemented(manager: SillyManager, event: SillyEvent):
    await manager.show_popup(event.user, SillyDefaults.Options.NOT_IMPLEMENTED_TEXT)


@SillyManager.priveleged()
async def _on_stats_button_clicked(manager: SillyManager, event: SillyEvent):
    await manager.show_popup(event.user, manager.stats)


@SillyManager.priveleged()
async def _on_priveleges_button_clicked(manager: SillyManager, event: SillyEvent):
    user_to_check = await get_user(manager, event)
    if not user_to_check:
        return

    privelege_name = user_to_check.privelege_name
    text_to_show = SillyDefaults.Options.NEGATIVE_PRIVELEGE_INFO.format(
        user_to_check.nickname_or_id
    )
    if privelege_name:
        text_to_show = SillyDefaults.Options.POSITIVE_PRIVELEGE_INFO.format(
            user_to_check.nickname_or_id, privelege_name
        )

    if not await manager.get_yes_no_answer(event.user, text_to_show):
        return

    privelege_options = (
        *[SillyText(text) for text in manager.priveleges_names],
        SillyDefaults.Options.DEFAULT_PRIVELEGE,
    )

    privelege_id = await manager.show_dialog(
        event.user,
        SillyDefaults.Options.PRIVEGELE_PROMPT.format(user_to_check.nickname_or_id),
        *privelege_options
    )

    if privelege_id is not None:
        text = SillyDefaults.Options.PRIVELEGE_NEGATIVE_SETTING_SUCCESS.format(
            user_to_check.nickname_or_id
        )
        if privelege_id in range(len(manager.priveleges_names)):
            text = SillyDefaults.Options.PRIVELEGE_POSITIVE_SETTING_SUCCESS.format(
                user_to_check.nickname_or_id, manager.priveleges_names[privelege_id]
            )
            manager.set_privelege(user_to_check, manager.priveleges_names[privelege_id])
        else:
            manager.set_privelege(user_to_check, None)

        await manager.show_popup(event.user, text)


options_page = SillyPage(
    name=SillyDefaults.Names.OPTIONS_PAGE,
    text=SillyDefaults.Options.ROOT_PAGE_TEXT,
    buttons=(
        (
            NavigationSillyButton(
                SillyDefaults.Options.COMMUNICATION_BUTTON_TEXT,
                SillyDefaults.Options.CommunicationPage.NAME,
            ),
        ),
        (
            ActionSillyButton(
                SillyDefaults.Options.PRIVELEGES_BUTTON_TEXT,
                _on_priveleges_button_clicked,
            ),
            ActionSillyButton(
                SillyDefaults.Options.STATS_BUTTON_TEXT, _on_stats_button_clicked
            ),
            NavigationSillyButton(
                SillyDefaults.Options.BANNED_BUTTON_TEXT,
                SillyDefaults.Options.BannedPage.NAME,
            ),
        ),
        (
            NavigationSillyButton(
                SillyDefaults.Options.HOME_BUTTON_TEXT,
                SillyDefaults.Names.HOME_PAGE,
            ),
            NavigationSillyButton(
                SillyDefaults.Options.MORE_BUTTON_TEXT,
                SillyDefaults.Names.MORE_OPTIONS_PAGE,
                not_found_message=SillyDefaults.Options.MORE_OPTIONS_PAGE_TEMPLATE_TEXT,
            ),
        ),
    ),
)
