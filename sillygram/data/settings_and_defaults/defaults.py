from dataclasses import dataclass
from ...text import SillyText


@dataclass(frozen=True)
class SillyDefaults:
    @dataclass(frozen=True)
    class CallbackData:
        CONTINUE = "CONTINUE"
        CONFIRM = "CONFIRM"
        BACK = "BACK"
        CLOSE = "CLOSE"
        CANCEL = "CANCEL"
        OPTION_TEMPLATE = "OPTION_"
        CANCEL_OPTION = "OPTION_CANCEL"
        BUTTON_TEMPLATE = "Button-[{}]"

        DEFAULT = "DEFAULT"

        HOME_COMMAND = "home"
        START_COMMAND = "start"
        INPUT_CANCEL_MARKER = "$INPUT_CANCELLED$"

    @dataclass(frozen=True)
    class Names:
        START_PAGE = "START"
        HOME_PAGE = "HOME"
        OPTIONS_PAGE = "OPTIONS"
        MORE_OPTIONS_PAGE = "MORE_OPTIONS"

    @dataclass(frozen=True)
    class Priveleges:
        ADMIN_PRIVELEGY_NAME = "Administrator"

    @dataclass(frozen=True)
    class Options:
        ROOT_PAGE_TEXT = SillyText("This is the SillyGram options page")
        BANNED_BUTTON_TEXT = SillyText("Banned")
        PRIVELEGES_BUTTON_TEXT = SillyText("Priveleges")

        POSITIVE_PRIVELEGE_INFO = SillyText(
            "Current privelege for {} is {}.\n\nWould you like to change it?"
        )
        NEGATIVE_PRIVELEGE_INFO = SillyText(
            "User {} currently does not possess any priveleges.\n\nWould you like to change it?"
        )
        PRIVEGELE_PROMPT = SillyText("What privelege status should be given to {}?")
        DEFAULT_PRIVELEGE = SillyText("No priveleges")
        PRIVELEGE_POSITIVE_SETTING_SUCCESS = SillyText("User {} is now {}")
        PRIVELEGE_NEGATIVE_SETTING_SUCCESS = SillyText("User {} does not have any priveleges anymore.")

        ADMINS_BUTTON_TEXT = SillyText("Admins")
        COMMUNICATION_BUTTON_TEXT = SillyText("Communication")
        STATS_BUTTON_TEXT = SillyText("Stats")
        HOME_BUTTON_TEXT = SillyText("Home")
        RESET_BUTTON_TEXT = SillyText("Reset data")
        REGISTRY_BUTTON_TEXT = SillyText("Registry")
        NOT_IMPLEMENTED_TEXT = SillyText(
            "This will be implemented in future versions of SillyGram!"
        )

        DATETIME_FORMAT = SillyText("%d.%m.%Y-%H:%M")

        BACK_BUTTON_TEXT = SillyText("Back")
        USER_ID_INPUT_PROMPT = SillyText("Please enter the user name of ID")
        ERROR_MESSAGE_TEMPLATE = SillyText("An error has occurred.\n\n{}")

        USER_NOT_REGISTERED_ERROR_TEMPLATE = SillyText("User {} not registered")
        MORE_BUTTON_TEXT = SillyText("More")
        MORE_PAGE_PLACEHOLDER = SillyText("There is no such page...")

        @dataclass(frozen=True)
        class AdminsPage:
            NAME = "ADMINS"
            TEXT = SillyText("Admins page")
            PROMOTE_BUTTON_TEXT = SillyText("Promote")
            DEMOTE_BUTTON_TEXT = SillyText("Demote")
            LIST_BUTTON_TEXT = SillyText("List")
            LIST_MESSAGE_TEMPLATE = SillyText("Admins list:\n\n{}")
            LIST_MESSAGE_EMPTY = SillyText("There are no admins")

            PROMOTION_USER_ID_INPUT_PROMPT = SillyText(
                "Please enter the ID of the user you want to promote."
            )
            DEMOTION_USER_ID_INPUT_PROMPT = SillyText(
                "Please enter the ID of the user you want to demote."
            )

            PROMOTION_SUCCESS_MESSAGE_TEMPLATE = SillyText(
                "User {} has been successfully promoted."
            )
            DEMOTION_SUCCESS_MESSAGE_TEMPLATE = SillyText(
                "User {} has been successfully demoted."
            )

            PROMOTION_CONFIRMATION_PROMPT = SillyText(
                "Are you sure you want to promote user {}?\n\n"
                "This will grant them administrator permission, "
                "which will provide them with the access to the "
                "SG control panel you are currently using so that "
                "they could ban and unban users, grant or take away other users "
                "admin permission (including you as well) and reset all the bot data!"
            )

            DEMOTION_CONFIRMATION_PROMPT = SillyText(
                "Are you sure you want to demote user {}?\n\n"
                "This will take away their administration permission "
                "so that they will not be able to access the SG control panel anymore."
            )

        @dataclass(frozen=True)
        class BannedPage:
            NAME = "BANNED"
            TEXT = SillyText("Banned page")
            LIST_MESSAGE_TEMPLATE = SillyText("SillyText(Banned users list:\n\n{}")

            BAN_USER_ID_INPUT_PROMPT = SillyText(
                "Please enter the ID of the user you want to ban."
            )
            BAN_DATE_INPUT_PROMPT = SillyText(
                "Now enter the blocking duration in days (non integral values are allowed)"
            )
            BAN_DURATION_DIALOG_TEXT = SillyText("Choose ban duration")
            AMNESTY_DIALOG_TEXT = SillyText(
                "Are you sure you want to perform amnesty? All the users will be unbanned."
            )

            AMNESTY_SUCCESS_TEXT = SillyText("There are no banned users anymore.")

            ONE_DAY_BAN_OPTION = SillyText("1 day")
            ONE_WEEK_BAN_OPTION = SillyText("1 week")
            ONE_MONTH_BAN_OPTION = SillyText("1 month")
            ONE_YEAR_BAN_OPTION = SillyText("1 year")
            CUSTOM_BAN_OPTION = SillyText("Custom")
            PERMANENT_BAN_OPTION = SillyText("Permanent")
            CANCEL_BAN_OPTION = SillyText("Cancel")

            UNBAN_USER_ID_INPUT_PROMPT = SillyText(
                "Please enter the ID of the user you want to unban."
            )

            TEMPORAL_BAN_SUCCESS_MESSAGE_TEMPLATE = SillyText(
                "User {} is now banned until {}."
            )
            PERMANENT_BAN_SUCCESS_MESSAGE_TEMPLATE = SillyText(
                "User {} is now banned permanently."
            )

            UNBAN_SUCCESS_MESSAGE_TEMPLATE = SillyText("User {} is not banned anymore.")

            BAN_BUTTON_TEXT = SillyText("Ban")
            UNBAN_BUTTON_TEXT = SillyText("Unban")
            AMNESTY_BUTTON_TEXT = SillyText("Amnesty")
            LIST_BUTTON_TEXT = SillyText("List")

            LIST_MESSAGE_TEMPLATE = SillyText("Banned users list:\n\n{}")
            NO_BANNED_USERS_MESSAGE = SillyText("There are no banned users.")
            BANNED_USER_LINE_TEMPLATE = SillyText("User {} is banned until {}.")

            DAYS_PARSING_ERROR_TEXT = SillyText("Invalid input format.")

        @dataclass(frozen=True)
        class CommunicationPage:
            NAME = "COMMUNICATION"
            TEXT = SillyText("Communication page")

            SEND_MESSAGE_BUTTON_TEXT = SillyText("Personal message")
            BROADCAST_BUTTON_TEXT = SillyText("Broadcast message")

            PERSONAL_MESSAGE_TEXT = SillyText("Please enter the text you want to send to {}.")
            BROADCAST_MESSAGE_TEXT = SillyText("Please enter the text you want to broadcast.")

            MESSAGE_RECEIVED_TEMPLATE = SillyText("{}\n<blockquote>{}</blockquote>")
            MESSAGE_DELIVERED_TEXT = SillyText("Your message has been delivered to {}.")
    
            BROADCAST_SUCCESS_TEXT = SillyText("Broadcast has been successfully started.")

        class BroadcastStatusPage:
            NAME = "BROADCAST_RUNNING"
            TEXT = SillyText("There is already a broadcast running. Please wait.\n\nAt the moment {} of {} messages have been sent. ({}%)")

            REFRESH_BUTTON_TEXT = SillyText("Refresh")
            STOP_BROADCAST_BUTTON_TEXT = SillyText("Stop")

            STOP_CONFIRMATION_TEXT = SillyText("Are you sure you want to stop the broadcast?")
            BROADCAST_STOPPED_TEXT = SillyText("Broadcast has been stopped.")

        @dataclass(frozen=True)
        class RegistryPage:
            NAME = "REGISTRY"

        @dataclass(frozen=True)
        class StatsPage:
            NAME = "STATS"

        MORE_OPTIONS_PAGE_TEMPLATE_TEXT = SillyText("There is no such page...")

    # region Commands
    @dataclass(frozen=True)
    class Commands:
        START = "start"
        HOME = "home"
        OPTIONS = "options"

    @dataclass(frozen=True)
    class CLI:

        @dataclass(frozen=True)
        class Messages:
            PRIVELEGE_NOT_MENTIONED_TEMPLATE = "Privelege named '{}' found in DB, but was not specified in SillySettings"
            PRIVELEGE_NOT_FOUND_TEMPLATE = "Privelege named '{}' is unknown."
            USER_WITH_UNKNOWN_PRIVELEGE = "User {} has an unknown privelege '{}'."


SILLY_START_PAGE_POINTER = SillyDefaults.Names.START_PAGE
SILLY_HOME_PAGE_POINTER = SillyDefaults.Names.HOME_PAGE
