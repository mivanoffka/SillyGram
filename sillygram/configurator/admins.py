from ..ui import ActionSillyButton, SillyPage, NavigationSillyButton
from ..data import SillyDefaults
from ..events import SillyEvent
from ..manager import SillyManager
from .common import get_user


@SillyManager.admin_only
async def _on_promote_button_click(manager: SillyManager, event: SillyEvent):
    user_to_promote = await get_user(manager, event)
    if not user_to_promote:
        return

    uinfo = (
        str(user_to_promote.id)
        if not user_to_promote.nickname
        else "{} ({})".format(user_to_promote.nickname, user_to_promote.id)
    )
    confirmation = await manager.get_yes_no_answer(
        event.user,
        SillyDefaults.Configurator.AdminsPage.PROMOTION_CONFIRMATION_PROMPT.format(
            uinfo
        ),
    )

    if not confirmation:
        await manager.refresh_page(event.user)
        return

    try:
        manager.users.promote(user_to_promote.id)

        await manager.show_message(
            event.user,
            SillyDefaults.Configurator.AdminsPage.PROMOTION_SUCCESS_MESSAGE_TEMPLATE.format(
                uinfo
            ),
        )

    except Exception as e:
        await manager.show_message(
            event.user, SillyDefaults.Configurator.ERROR_MESSAGE_TEMPLATE.format(e)
        )
        return


@SillyManager.admin_only
async def _on_demote_button_click(manager: SillyManager, event: SillyEvent):
    user_to_demote = await get_user(manager, event)
    if not user_to_demote:
        return

    uinfo = (
        str(user_to_demote.id)
        if not user_to_demote.nickname
        else "{} ({})".format(user_to_demote.nickname, user_to_demote.id)
    )
    confirmation = await manager.get_yes_no_answer(
        event.user,
        SillyDefaults.Configurator.AdminsPage.DEMOTION_CONFIRMATION_PROMPT.format(
            uinfo
        ),
    )

    if not confirmation:
        await manager.refresh_page(event.user)
        return

    try:
        manager.users.demote(user_to_demote.id)

        await manager.show_message(
            event.user,
            SillyDefaults.Configurator.AdminsPage.DEMOTION_SUCCESS_MESSAGE_TEMPLATE.format(
                uinfo
            ),
        )

    except Exception as e:
        await manager.show_message(
            event.user, SillyDefaults.Configurator.ERROR_MESSAGE_TEMPLATE.format(str(e))
        )
        return


@SillyManager.admin_only
async def _on_list_button_click(manager: SillyManager, event: SillyEvent):
    admins_list = manager.users.get_all_admins()
    message_text = SillyDefaults.Configurator.AdminsPage.LIST_MESSAGE_EMPTY
    if admins_list:
        admins_list_str = ""
        for admin in admins_list:
            admins_list_str += (
                str(admin.id)
                if not admin.nickname
                else "{} ({})".format(admin.nickname, admin.id) + "\n"
            )

        message_text = (
            SillyDefaults.Configurator.AdminsPage.LIST_MESSAGE_TEMPLATE.format(
                admins_list_str
            )
        )
    await manager.show_message(event.user, message_text)


admins_page = SillyPage(
    name=SillyDefaults.Configurator.AdminsPage.NAME,
    text=SillyDefaults.Configurator.AdminsPage.TEXT,
    buttons=(
        (
            ActionSillyButton(
                SillyDefaults.Configurator.AdminsPage.PROMOTE_BUTTON_TEXT,
                _on_promote_button_click,
            ),
            ActionSillyButton(
                SillyDefaults.Configurator.AdminsPage.DEMOTE_BUTTON_TEXT,
                _on_demote_button_click,
            ),
            ActionSillyButton(
                SillyDefaults.Configurator.AdminsPage.LIST_BUTTON_TEXT,
                _on_list_button_click,
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
