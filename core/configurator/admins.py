from ..ui import ActionButton, SillyPage, NavigationButton
from ..data import SillyDefaults
from ..management import SillyManager, SillyEvent


async def _on_promote_button_click(manager: SillyManager, event: SillyEvent):
    uid = await manager.get_input(event.user, SillyDefaults.Configurator.AdminsPage.PROMOTION_USER_ID_INPUT_PROMPT)
    confirmation = await manager.get_yes_no_answer(event.user, SillyDefaults.Configurator.AdminsPage.
                                                   PROMOTION_CONFIRMATION_PROMPT.format(uid))

    if not confirmation:
        await manager.refresh_page(event.user)
        return

    try:
        await manager.promote(uid)
    except Exception as e:
        await manager.show_message(event.user, SillyDefaults.Configurator.ERROR_MESSAGE_TEMPLATE.format(e))
        return

    await manager.show_message(event.user, SillyDefaults.Configurator.AdminsPage.
                               PROMOTION_SUCCESS_MESSAGE_TEMPLATE.format(uid))


async def _on_demote_button_click(manager: SillyManager, event: SillyEvent):
    uid = await manager.get_input(event.user, SillyDefaults.Configurator.AdminsPage.DEMOTION_USER_ID_INPUT_PROMPT)
    confirmation = await manager.get_yes_no_answer(event.user, SillyDefaults.Configurator.AdminsPage.
                                                   DEMOTION_CONFIRMATION_PROMPT.format(uid))

    if not confirmation:
        await manager.refresh_page(event.user)
        return

    try:
        await manager.demote(uid)
    except Exception as e:
        await manager.show_message(event.user, SillyDefaults.Configurator.ERROR_MESSAGE_TEMPLATE.format(e))
        return

    await manager.show_message(event.user, SillyDefaults.Configurator.AdminsPage.
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
