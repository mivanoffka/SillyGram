from datetime import timedelta
from typing import Optional

from ..ui import SillyActionButton, SillyPage, SillyNavigationButton
from ..data import SillyDefaults
from ..user import SillyUser
from ..events import SillyEvent
from ..manager import SillyManager

from .common import get_user


@SillyManager.priveleged()
async def _on_banned_button_click(manager: SillyManager, event: SillyEvent):
    user_to_ban: Optional[SillyUser]
    user_to_ban = await get_user(manager, event)
    if not user_to_ban:
        return

    option = await manager.show_dialog(
        event.user,
        SillyDefaults.Options.BannedPage.BAN_DURATION_DIALOG_TEXT,
        SillyDefaults.Options.BannedPage.ONE_DAY_BAN_OPTION,
        SillyDefaults.Options.BannedPage.ONE_WEEK_BAN_OPTION,
        SillyDefaults.Options.BannedPage.ONE_MONTH_BAN_OPTION,
        SillyDefaults.Options.BannedPage.ONE_YEAR_BAN_OPTION,
        SillyDefaults.Options.BannedPage.CUSTOM_BAN_OPTION,
        SillyDefaults.Options.BannedPage.PERMANENT_BAN_OPTION,
        SillyDefaults.Options.BannedPage.CANCEL_BAN_OPTION,
    )

    duration = 24
    multiplier = -1
    if option == 0:
            multiplier = 1
    if option == 1:
            multiplier = 7
    if option == 2:
            multiplier = 30
    if option == 3:
            multiplier = 365
    if option == 4:
            input_text = await manager.get_input(
                event.user, SillyDefaults.Options.BannedPage.BAN_DATE_INPUT_PROMPT
            )
            try:
                if not input_text:
                    raise Exception()

                if "," in input_text:
                    input_text = input_text.replace(",", ".")
                value = float(input_text)
                if value <= 0:
                    raise ValueError()
                multiplier = round(value, 2)
            except Exception:
                await manager.show_popup(
                    event.user,
                    SillyDefaults.Options.ERROR_MESSAGE_TEMPLATE.format(
                        SillyDefaults.Options.BannedPage.DAYS_PARSING_ERROR_TEXT
                    ),
                )
                return
    if option == 5:
            multiplier = 9999
    if option == 6:
            await manager.restore_page(event.user)
            return

    try:
        duration *= multiplier
        expires = manager.users.ban(user_to_ban.id, timedelta(hours=int(duration)))

        uinfo = (
            str(user_to_ban.id)
            if not user_to_ban.nickname
            else "{} ({})".format(user_to_ban.nickname, user_to_ban.id)
        )
        await manager.show_popup(
            event.user,
            SillyDefaults.Options.BannedPage.TEMPORAL_BAN_SUCCESS_MESSAGE_TEMPLATE.format(
                uinfo,
                expires.strftime(
                    SillyDefaults.Options.DATETIME_FORMAT.localize(
                        event.user.language_code
                    )
                ),
            ),
        )
    except Exception as e:
        await manager.show_popup(
            event.user, SillyDefaults.Options.ERROR_MESSAGE_TEMPLATE.format(e)
        )


@SillyManager.priveleged()
async def _on_unban_button_click(manager: SillyManager, event: SillyEvent):
    user_to_unban = await get_user(manager, event)
    if user_to_unban is None:
        return

    try:
        manager.users.unban(user_to_unban.id)
        uinfo = (
            str(user_to_unban.id)
            if not user_to_unban.nickname
            else "{} ({})".format(user_to_unban.nickname, user_to_unban.id)
        )
        await manager.show_popup(
            event.user,
            SillyDefaults.Options.BannedPage.UNBAN_SUCCESS_MESSAGE_TEMPLATE.format(
                uinfo
            ),
        )

    except Exception as e:
        await manager.show_popup(
            event.user, SillyDefaults.Options.ERROR_MESSAGE_TEMPLATE.format(e)
        )
        return


@SillyManager.priveleged()
async def _on_amnesty_button_click(manager: SillyManager, event: SillyEvent):
    confirmed = await manager.get_yes_no_answer(
        event.user, SillyDefaults.Options.BannedPage.AMNESTY_DIALOG_TEXT
    )
    if not confirmed:
        await manager.restore_page(event.user)
        return

    try:
        manager.users.unban_all()
        await manager.show_popup(
            event.user, SillyDefaults.Options.BannedPage.AMNESTY_SUCCESS_TEXT
        )
    except Exception as e:
        await manager.show_popup(
            event.user, SillyDefaults.Options.ERROR_MESSAGE_TEMPLATE.format(e)
        )


@SillyManager.priveleged()
async def _on_list_button_click(manager: SillyManager, event: SillyEvent):
    banned_users_list = manager.users.get_all_banned()
    message_text = SillyDefaults.Options.BannedPage.NO_BANNED_USERS_MESSAGE
    if banned_users_list:
        lines = ""
        for banned_user in banned_users_list:

            uinfo = (
                str(banned_user.id)
                if not banned_user.nickname
                else "{} ({})".format(banned_user.nickname, banned_user.id)
            )
            exp_date = banned_user.ban_expiration_date
            if exp_date is None:
                exp_date = "?"
            else:
                exp_date = exp_date.strftime(
                    SillyDefaults.Options.DATETIME_FORMAT.localize(
                        event.user.language_code
                    )
                )
            lines += (
                SillyDefaults.Options.BannedPage.BANNED_USER_LINE_TEMPLATE.format(
                    uinfo, exp_date
                ).localize(event.user.language_code)
            )
        message_text = (
            SillyDefaults.Options.BannedPage.LIST_MESSAGE_TEMPLATE.format(lines)
        )

    await manager.show_popup(event.user, message_text)


banned_page = SillyPage(
    name=SillyDefaults.Options.BannedPage.NAME,
    text=SillyDefaults.Options.BannedPage.TEXT,
    buttons=(
        (
            SillyActionButton(
                SillyDefaults.Options.BannedPage.BAN_BUTTON_TEXT,
                _on_banned_button_click,
            ),
            SillyActionButton(
                SillyDefaults.Options.BannedPage.UNBAN_BUTTON_TEXT,
                _on_unban_button_click,
            ),
            SillyActionButton(
                SillyDefaults.Options.BannedPage.AMNESTY_BUTTON_TEXT,
                _on_amnesty_button_click,
            ),
        ),
        (
            SillyNavigationButton(
                SillyDefaults.Options.BACK_BUTTON_TEXT,
                SillyDefaults.Names.OPTIONS_PAGE,
            ),
            SillyActionButton(
                SillyDefaults.Options.BannedPage.LIST_BUTTON_TEXT,
                _on_list_button_click,
            ),
        ),
    ),
)
