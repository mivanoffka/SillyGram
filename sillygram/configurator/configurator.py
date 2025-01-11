from sillygram import privelege
from ..ui import ActionSillyButton, SillyPage, NavigationSillyButton
from ..data import SillyDefaults
from ..manager import SillyManager
from ..text import SillyText
from ..events import SillyEvent
from .common import get_user


@SillyManager.protected()
async def _not_implemented(manager: SillyManager, event: SillyEvent):
    await manager.show_popup(
        event.user, SillyDefaults.Configurator.NOT_IMPLEMENTED_TEXT
    )


@SillyManager.protected()
async def _on_stats_button_clicked(manager: SillyManager, event: SillyEvent):
    await manager.show_popup(event.user, manager.stats)


@SillyManager.protected()
async def _on_priveleges_button_clicked(manager: SillyManager, event: SillyEvent):
    user_to_check = await get_user(manager, event)
    if not user_to_check:
        return

    privelege_name = user_to_check.privelege_name
    text_to_show = SillyDefaults.Configurator.NEGATIVE_PRIVELEGE_INFO.format(
        user_to_check.nickname_or_id
    )
    if privelege_name:
        text_to_show = SillyDefaults.Configurator.POSITIVE_PRIVELEGE_INFO.format(
            user_to_check.nickname_or_id, privelege_name
        )

    if not await manager.get_yes_no_answer(event.user, text_to_show):
        return

    privelege_options = (
        *[SillyText(text) for text in manager.priveleges_names],
        SillyDefaults.Configurator.DEFAULT_PRIVELEGE,
    )

    privelege_id = await manager.show_dialog(
        event.user,
        SillyDefaults.Configurator.PRIVEGELE_PROMPT.format(
            user_to_check.nickname_or_id
        ),
        *privelege_options
    )

    if privelege_id is not None:
        text = SillyDefaults.Configurator.PRIVELEGE_NEGATIVE_SETTING_SUCCESS.format(
            user_to_check.nickname_or_id
        )
        if privelege_id in range(len(manager.priveleges_names)):
            text = SillyDefaults.Configurator.PRIVELEGE_POSITIVE_SETTING_SUCCESS.format(
                user_to_check.nickname_or_id, manager.priveleges_names[privelege_id]
            )
            manager.set_privelege(user_to_check, manager.priveleges_names[privelege_id])
        else:
            manager.set_privelege(user_to_check, None)

        await manager.show_popup(event.user, text)


configuration_page = SillyPage(
    name=SillyDefaults.Names.CONFIGURE_PAGE,
    text=SillyDefaults.Configurator.ROOT_PAGE_TEXT,
    buttons=(
        (
            ActionSillyButton(
                SillyDefaults.Configurator.STATS_BUTTON_TEXT, _on_stats_button_clicked
            ),
        ),
        (
            ActionSillyButton(
                SillyDefaults.Configurator.PRIVELEGES_BUTTON_TEXT,
                _on_priveleges_button_clicked,
            ),
            NavigationSillyButton(
                SillyDefaults.Configurator.BANNED_BUTTON_TEXT,
                SillyDefaults.Configurator.BannedPage.NAME,
            ),
        ),
        (
            NavigationSillyButton(
                SillyDefaults.Configurator.HOME_BUTTON_TEXT,
                SillyDefaults.Names.HOME_PAGE,
            ),
        ),
    ),
)
