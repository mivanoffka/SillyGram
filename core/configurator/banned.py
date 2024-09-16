from datetime import timedelta
from typing import Optional

from ..ui import ActionButton, SillyPage, NavigationButton
from ..data import SillyDefaults, SillyUser
from ..management import SillyManager

from .utility import get_user_name_or_id


async def _on_banned_button_click(manager: SillyManager, user: SillyUser):
    user: SillyUser
    try:
        user = await get_user_name_or_id(manager, user, SillyDefaults.Configurator.BannedPage.BAN_USER_ID_INPUT_PROMPT)
    except Exception as e:
        await manager.show_message(user, SillyDefaults.Configurator.ERROR_MESSAGE_TEMPLATE.format(e))
        return

    option = await manager.show_dialog(user, SillyDefaults.Configurator.BannedPage.BAN_DURATION_DIALOG_TEXT,
                                       SillyDefaults.Configurator.BannedPage.ONE_DAY_BAN_OPTION,
                                       SillyDefaults.Configurator.BannedPage.ONE_WEEK_BAN_OPTION,
                                       SillyDefaults.Configurator.BannedPage.ONE_MONTH_BAN_OPTION,
                                       SillyDefaults.Configurator.BannedPage.ONE_YEAR_BAN_OPTION,
                                       SillyDefaults.Configurator.BannedPage.CUSTOM_BAN_OPTION,
                                       SillyDefaults.Configurator.BannedPage.PERMANENT_BAN_OPTION,
                                       SillyDefaults.Configurator.BannedPage.CANCEL_BAN_OPTION)

    duration = 24
    multiplier = -1
    match option:
        case 0:
            multiplier = 1
        case 1:
            multiplier = 7
        case 2:
            multiplier = 30
        case 3:
            multiplier = 365
        case 4:
            input_text = await manager.get_input(user,
                                                 SillyDefaults.Configurator.BannedPage.BAN_DATE_INPUT_PROMPT)
            try:
                if "," in input_text:
                    input_text = input_text.replace(",", ".")
                value = float(input_text)
                if value <= 0:
                    raise ValueError()
                multiplier = round(value, 2)
            except Exception as e:
                await manager.show_message(user, SillyDefaults.Configurator.ERROR_MESSAGE_TEMPLATE
                                           .format(SillyDefaults.Configurator.BannedPage.DAYS_PARSING_ERROR_TEXT))
                return
        case 5:
            multiplier = 9999
        case 6:
            await manager.refresh_page(user)

    try:
        duration *= multiplier
        expires = await manager.users.ban(user.id, timedelta(hours=int(duration)))

        uinfo = str(user.id) if not user.nickname else "{} ({})".format(user.nickname, user.id)
        await manager.show_message(user, SillyDefaults.Configurator.BannedPage
                                   .TEMPORAL_BAN_SUCCESS_MESSAGE_TEMPLATE.format(uinfo, expires))
        return
    except Exception as e:
        await manager.show_message(user, SillyDefaults.Configurator.ERROR_MESSAGE_TEMPLATE.format(e))


async def _on_unban_button_click(manager: SillyManager, user: SillyUser):
    user: SillyUser
    try:
        user = await get_user_name_or_id(manager, user, SillyDefaults.Configurator.BannedPage.
                                         UNBAN_USER_ID_INPUT_PROMPT)
    except Exception as e:
        await manager.show_message(user, SillyDefaults.Configurator.ERROR_MESSAGE_TEMPLATE.format(e))
        return

    try:
        await manager.users.unban(user.id)
        uinfo = str(user.id) if not user.nickname else "{} ({})".format(user.nickname, user.id)
        await manager.show_message(user, SillyDefaults.Configurator.BannedPage
                                   .UNBAN_SUCCESS_MESSAGE_TEMPLATE.format(uinfo))

    except Exception as e:
        await manager.show_message(user, SillyDefaults.Configurator.ERROR_MESSAGE_TEMPLATE
                                   .format(e))
        return


async def _on_amnesty_button_click(manager: SillyManager, user: SillyUser):
    confirmed = await manager.get_yes_no_answer(user, SillyDefaults.Configurator.BannedPage.AMNESTY_DIALOG_TEXT)
    if not confirmed:
        await manager.refresh_page(user)
        return

    try:
        manager.users.amnesty()
        await manager.show_message(user, SillyDefaults.Configurator.BannedPage.AMNESTY_SUCCESS_TEXT)
    except Exception as e:
        await manager.show_message(user, SillyDefaults.Configurator.ERROR_MESSAGE_TEMPLATE.format(e))


banned_page = SillyPage(name=SillyDefaults.Configurator.BannedPage.NAME,
                        text=SillyDefaults.Configurator.BannedPage.TEXT,
                        buttons=(
                            (ActionButton(SillyDefaults.Configurator.BannedPage.BAN_BUTTON_TEXT,
                                          _on_banned_button_click),
                             ActionButton(SillyDefaults.Configurator.BannedPage.UNBAN_BUTTON_TEXT,
                                          _on_unban_button_click),
                             ActionButton(SillyDefaults.Configurator.BannedPage.AMNESTY_BUTTON_TEXT,
                                          _on_amnesty_button_click),),
                            (NavigationButton(SillyDefaults.Configurator.BACK_BUTTON_TEXT,
                                              SillyDefaults.Names.CONFIGURE_PAGE),
                             ActionButton(SillyDefaults.Configurator.BannedPage.LIST_BUTTON_TEXT))

                        ))
