from datetime import timedelta
from typing import Optional

from ..ui import ActionButton, SillyPage, NavigationButton
from ..data import SillyDefaults
from ..user import SillyUser
from ..manager import SillyManager


async def _on_banned_button_click(manager: SillyManager, user: SillyUser):
    user_to_ban: SillyUser
    input_str = "?"
    try:
        input_str = await manager.get_input(user, SillyDefaults.Configurator.USER_ID_INPUT_PROMPT)
        user_to_ban = manager.users.get(input_str)
    except Exception as e:
        await manager.show_message(user, SillyDefaults.Configurator.ERROR_MESSAGE_TEMPLATE.format(
            SillyDefaults.Configurator.USER_NOT_REGISTERED_ERROR_TEMPLATE.format(input_str)
        ))
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
            return;

    try:
        duration *= multiplier
        expires = manager.users.ban(user_to_ban.id, timedelta(hours=int(duration)))

        uinfo = str(user_to_ban.id) if not user_to_ban.nickname else "{} ({})".format(user_to_ban.nickname, user_to_ban.id)
        await manager.show_message(user, SillyDefaults.Configurator.BannedPage
                                   .TEMPORAL_BAN_SUCCESS_MESSAGE_TEMPLATE.format(uinfo, expires.strftime(SillyDefaults.Configurator.DATETIME_FORMAT)))
    except Exception as e:
        await manager.show_message(user, SillyDefaults.Configurator.ERROR_MESSAGE_TEMPLATE.format(e))


async def _on_unban_button_click(manager: SillyManager, user: SillyUser):
    user_to_unban: SillyUser
    input_str = "?"
    try:
        input_str = await manager.get_input(user, SillyDefaults.Configurator.USER_ID_INPUT_PROMPT)
        user_to_unban = manager.users.get(input_str)
    except Exception as e:
        await manager.show_message(user, SillyDefaults.Configurator.ERROR_MESSAGE_TEMPLATE.format(
            SillyDefaults.Configurator.USER_NOT_REGISTERED_ERROR_TEMPLATE.format(input_str)
        ))
        return

    try:
        manager.users.unban(user_to_unban.id)
        uinfo = str(user_to_unban.id) if not user_to_unban.nickname else "{} ({})".format(user_to_unban.nickname, user_to_unban.id)
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
        manager.users.unban_all()
        await manager.show_message(user, SillyDefaults.Configurator.BannedPage.AMNESTY_SUCCESS_TEXT)
    except Exception as e:
        await manager.show_message(user, SillyDefaults.Configurator.ERROR_MESSAGE_TEMPLATE.format(e))


async def _on_list_button_click(manager: SillyManager, user: SillyUser):
    banned_users_list = manager.users.get_all_banned()
    message_text = SillyDefaults.Configurator.BannedPage.NO_BANNED_USERS_MESSAGE
    if banned_users_list:
        lines = ""
        for banned_user in banned_users_list:

            uinfo = str(banned_user.id) if not banned_user.nickname else "{} ({})".format(banned_user.nickname, banned_user.id)
            lines += (SillyDefaults.Configurator.BannedPage.BANNED_USER_LINE_TEMPLATE.
                      format(uinfo, banned_user.ban_expiration_date.strftime(SillyDefaults.Configurator.DATETIME_FORMAT)))
        message_text = SillyDefaults.Configurator.BannedPage.LIST_MESSAGE_TEMPLATE.format(lines)

    await user.show_message(message_text)


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
                             ActionButton(SillyDefaults.Configurator.BannedPage.LIST_BUTTON_TEXT,
                                          _on_list_button_click))

                        ))
