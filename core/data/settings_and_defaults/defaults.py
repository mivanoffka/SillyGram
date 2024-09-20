from dataclasses import dataclass


@dataclass(frozen=True)
class SillyDefaults:
    @dataclass(frozen=True)
    class CallbackData:
        CONTINUE = "CONTINUE"
        BACK = "BACK"
        CLOSE = "CLOSE"
        CANCEL = "CANCEL"
        OPTION_TEMPLATE = "OPTION_"
        BUTTON_TEMPLATE = "Button-[{}]"

        HOME_PAGE_NAME = "HOME"
        START_PAGE_NAME = "START"

        HOME_COMMAND = "home"
        START_COMMAND = "start"

    @dataclass(frozen=True)
    class Names:
        START_PAGE = "START"
        HOME_PAGE = "HOME"
        CONFIGURE_PAGE = "CONFIGURE"

    @dataclass(frozen=True)
    class Configurator:
        ROOT_PAGE_TEXT = "This is the SillyGram control page"
        BANNED_BUTTON_TEXT = "Banned"
        ADMINS_BUTTON_TEXT = "Admins"
        STATS_BUTTON_TEXT = "Stats"
        HOME_BUTTON_TEXT = "Home"
        RESET_BUTTON_TEXT = "Reset data"
        REGISTRY_BUTTON_TEXT = "Registry"

        DATETIME_FORMAT = "%d.%m.%Y-%H:%M"

        BACK_BUTTON_TEXT = "Back"
        USER_ID_INPUT_PROMPT = "Please enter the user name of ID"
        ERROR_MESSAGE_TEMPLATE = "An error has occurred.\n\n{}"

        USER_NOT_REGISTERED_ERROR_TEMPLATE = "User {} not registered"

        @dataclass(frozen=True)
        class AdminsPage:
            NAME = "ADMINS"
            TEXT = "Admins page"
            PROMOTE_BUTTON_TEXT = "Promote"
            DEMOTE_BUTTON_TEXT = "Demote"
            LIST_BUTTON_TEXT = "List"
            LIST_MESSAGE_TEMPLATE = "Admins list:\n\n{}"
            LIST_MESSAGE_EMPTY = "There are no admins"


            PROMOTION_USER_ID_INPUT_PROMPT = "Please enter the ID of the user you want to promote."
            DEMOTION_USER_ID_INPUT_PROMPT = "Please enter the ID of the user you want to demote."

            PROMOTION_SUCCESS_MESSAGE_TEMPLATE = "User {} has been successfully promoted."
            DEMOTION_SUCCESS_MESSAGE_TEMPLATE = "User {} has been successfully promoted."

            PROMOTION_CONFIRMATION_PROMPT = ("Are you sure you want to promote user {}?\n\n"
                                             "This will grant them administrator permission, "
                                             "which will provide them with the access to the "
                                             "SG control panel you are currently using so that "
                                             "they could ban and unban users, grant or take away other users "
                                             "admin permission (including you as well) and reset all the bot data!")

            DEMOTION_CONFIRMATION_PROMPT = ("Are you sure you want to demote user {}?\n\n"
                                            "This will take away their administration permission "
                                            "so that they will not be able to access the SG control panel anymore.")

        @dataclass(frozen=True)
        class BannedPage:
            NAME = "BANNED"
            TEXT = "Banned page"
            LIST_MESSAGE_TEMPLATE = "Banned users list:\n\n{}"

            BAN_USER_ID_INPUT_PROMPT = "Please enter the ID of the user you want to ban."
            BAN_DATE_INPUT_PROMPT = "Now enter the blocking duration in days (non integral values are allowed)"
            BAN_DURATION_DIALOG_TEXT = "Choose ban duration"
            AMNESTY_DIALOG_TEXT = "Are you sure you want to perform amnesty? All the users will be unbanned."

            AMNESTY_SUCCESS_TEXT = "There are no banned users anymore."

            ONE_DAY_BAN_OPTION = "1 day"
            ONE_WEEK_BAN_OPTION = "1 week"
            ONE_MONTH_BAN_OPTION = "1 month"
            ONE_YEAR_BAN_OPTION = "1 year"
            CUSTOM_BAN_OPTION = "Custom"
            PERMANENT_BAN_OPTION = "Permanent"
            CANCEL_BAN_OPTION = "Cancel"

            UNBAN_USER_ID_INPUT_PROMPT = "Please enter the ID of the user you want to unban."

            TEMPORAL_BAN_SUCCESS_MESSAGE_TEMPLATE = "User {} is now banned until {}."
            PERMANENT_BAN_SUCCESS_MESSAGE_TEMPLATE = "User {} is now banned permanently."

            UNBAN_SUCCESS_MESSAGE_TEMPLATE = "User {} is not banned anymore."

            BAN_BUTTON_TEXT = "Ban"
            UNBAN_BUTTON_TEXT = "Unban"
            AMNESTY_BUTTON_TEXT = "Amnesty"
            LIST_BUTTON_TEXT = "List"

            LIST_MESSAGE_TEMPLATE = "Banned users list:\n\n{}"
            NO_BANNED_USERS_MESSAGE = "There are no banned users."
            BANNED_USER_LINE_TEMPLATE = "User {} is banned until {}."

            DAYS_PARSING_ERROR_TEXT = "Invalid input format."

        @dataclass(frozen=True)
        class RegistryPage:
            NAME = "REGISTRY"

        @dataclass(frozen=True)
        class StatsPage:
            NAME = "STATS"

    # region Commands
    @dataclass(frozen=True)
    class Commands:
        START = "start"
        HOME = "home"
        CONFIGURE = "configure"
