from ..ui import ActionButton, SillyPage, NavigationButton
from ..data import SillyDefaults, SillyUser
from ..management import SillyManager


async def _on_promote_button_click(manager: SillyManager, user: SillyUser):
    uid = await manager.get_input(user, SillyDefaults.Configurator.AdminsPage.PROMOTION_USER_ID_INPUT_PROMPT)
    confirmation = await manager.get_yes_no_answer(user, SillyDefaults.Configurator.AdminsPage.
                                                   PROMOTION_CONFIRMATION_PROMPT.format(uid))

    if not confirmation:
        await manager.refresh_page(user)
        return

    try:
        await manager.users.promote(uid)
    except Exception as e:
        await manager.show_message(user, SillyDefaults.Configurator.ERROR_MESSAGE_TEMPLATE.format(e))
        return

    await manager.show_message(user, SillyDefaults.Configurator.AdminsPage.
                               PROMOTION_SUCCESS_MESSAGE_TEMPLATE.format(uid))


async def _on_demote_button_click(manager: SillyManager, user: SillyUser):
    uid = await manager.get_input(user, SillyDefaults.Configurator.AdminsPage.DEMOTION_USER_ID_INPUT_PROMPT)
    confirmation = await manager.get_yes_no_answer(user, SillyDefaults.Configurator.AdminsPage.
                                                   DEMOTION_CONFIRMATION_PROMPT.format(uid))

    if not confirmation:
        await manager.refresh_page(user)
        return

    try:
        await manager.users.demote(uid)
    except Exception as e:
        await manager.show_message(user, SillyDefaults.Configurator.ERROR_MESSAGE_TEMPLATE.format(e))
        return

    await manager.show_message(user, SillyDefaults.Configurator.AdminsPage.
                               DEMOTION_SUCCESS_MESSAGE_TEMPLATE.format(uid))


admins_page = SillyPage(name=SillyDefaults.Configurator.AdminsPage.NAME,
                        text=SillyDefaults.Configurator.AdminsPage.TEXT,
                        buttons=(
                            (ActionButton(SillyDefaults.Configurator.AdminsPage.PROMOTE_BUTTON_TEXT,
                                          _on_promote_button_click),
                             ActionButton(SillyDefaults.Configurator.AdminsPage.DEMOTE_BUTTON_TEXT,
                                          _on_demote_button_click),),
                            NavigationButton(SillyDefaults.Configurator.BACK_BUTTON_TEXT,
                                             SillyDefaults.Names.CONFIGURE_PAGE)
                        ))
