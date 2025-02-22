from dataclasses import dataclass
from ...text import SillyText

DEFAULT_NAME_TEMPLATE = "$-SILLYGRAM-DEFAULT-{}-{}-$"
PAGE_TYPE_NAME = "PAGE"
PRIVILEGE_TYPE_NAME = "privilege"
CALLBACK_TYPE_NAME = "CALLBACK"
MARKER_TYPE_NAME = "MARKER"


def _to_default_name(text: str, type: str) -> str:
    return DEFAULT_NAME_TEMPLATE.format(text, type)


@dataclass(frozen=True)
class SillyDefaults:

    @dataclass(frozen=True)
    class Registry:
        NOT_FOUND_MARKER = _to_default_name("NOT_FOUND", MARKER_TYPE_NAME)

    @dataclass(frozen=True)
    class CallbackData:
        CONTINUE = _to_default_name("CONTINUE", CALLBACK_TYPE_NAME)
        CONFIRM = _to_default_name("CONFIRM", CALLBACK_TYPE_NAME)
        BACK = _to_default_name("BACK", CALLBACK_TYPE_NAME)
        CLOSE = _to_default_name("CLOSE", CALLBACK_TYPE_NAME)
        CANCEL = _to_default_name("CANCEL", CALLBACK_TYPE_NAME)
        OPTION_TEMPLATE = _to_default_name("OPTION_", CALLBACK_TYPE_NAME)
        CANCEL_OPTION = _to_default_name("OPTION_CANCEL", CALLBACK_TYPE_NAME)
        BUTTON_TEMPLATE = _to_default_name("BUTTON-{}", CALLBACK_TYPE_NAME)

        DEFAULT = _to_default_name("DEFAULT", CALLBACK_TYPE_NAME)

        INPUT_CANCEL_MARKER = _to_default_name("INPUT_CANCELLED", MARKER_TYPE_NAME)

    @dataclass(frozen=True)
    class Names:
        class Pages:
            START = _to_default_name("START", PAGE_TYPE_NAME)
            HOME = _to_default_name("HOME", PAGE_TYPE_NAME)
            CONTROLS = _to_default_name("CONTROLS", PAGE_TYPE_NAME)
            CUSTOM_CONTROLS = _to_default_name("CUSTOM_CONTROLS", PAGE_TYPE_NAME)

        class PRIVILEGEs:
            MASTER = _to_default_name("MASTER", PRIVILEGE_TYPE_NAME)

    @dataclass(frozen=True)
    class Controls:
        ROOT_PAGE_TEXT = SillyText("This is the SillyGram controls page")
        BANNED_BUTTON_TEXT = SillyText("Banned")
        PRIVILEGES_BUTTON_TEXT = SillyText("PRIVILEGEs")

        POSITIVE_PRIVILEGE_INFO = SillyText(
            "Current privilege for {} is {}.\n\nWould you like to change it?"
        )
        NEGATIVE_PRIVILEGE_INFO = SillyText(
            "User {} currently does not possess any privileges.\n\nWould you like to change it?"
        )
        PRIVEGELE_PROMPT = SillyText("What privilege status should be given to {}?")
        DEFAULT_PRIVILEGE = SillyText("No privileges")
        PRIVILEGE_POSITIVE_SETTING_SUCCESS = SillyText("User {} is now {}")
        PRIVILEGE_NEGATIVE_SETTING_SUCCESS = SillyText(
            "User {} does not have any privileges anymore."
        )

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
        ADDITIONAL_CONTROLS_PAGE_TEMPLATE_TEXT = SillyText(
            "There is nothing here!\n\nHowever, bot developers can create a special page with additional control options for master-users that will be stored here."
        )

        @dataclass(frozen=True)
        class AdminsPage:
            NAME = _to_default_name("ADMINS", PAGE_TYPE_NAME)
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
            NAME = _to_default_name("BANNED", PAGE_TYPE_NAME)
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
            NAME = _to_default_name("COMMUNICATION", PAGE_TYPE_NAME)
            TEXT = SillyText("Communication page")

            SEND_MESSAGE_BUTTON_TEXT = SillyText("Personal message")
            BROADCAST_BUTTON_TEXT = SillyText("Broadcast message")

            PERSONAL_MESSAGE_TEXT = SillyText(
                "Please enter the text you want to send to {}."
            )
            BROADCAST_MESSAGE_TEXT = SillyText(
                "Please enter the text you want to broadcast."
            )

            MESSAGE_RECEIVED_TEMPLATE = SillyText("{}\n<blockquote>{}</blockquote>")
            MESSAGE_DELIVERED_TEXT = SillyText("Your message has been delivered to {}.")

            BROADCAST_SUCCESS_TEXT = SillyText(
                "Broadcast has been successfully started."
            )

        class BroadcastStatusPage:
            NAME = _to_default_name("BROADCAST_RUNNING", PAGE_TYPE_NAME)
            TEXT = SillyText(
                "There is already a broadcast running. Please wait.\n\nAt the moment {} of {} messages have been sent. ({}%)"
            )

            REFRESH_BUTTON_TEXT = SillyText("Refresh")
            STOP_BROADCAST_BUTTON_TEXT = SillyText("Stop")

            STOP_CONFIRMATION_TEXT = SillyText(
                "Are you sure you want to stop the broadcast?"
            )
            BROADCAST_STOPPED_TEXT = SillyText("Broadcast has been stopped.")

    # region Commands
    @dataclass(frozen=True)
    class Commands:
        START = "start"
        HOME = "home"
        CONTROLS = "controls"

    @dataclass(frozen=True)
    class CLI:
        @dataclass(frozen=True)
        class Messages:
            PRIVILEGE_NOT_MENTIONED_TEMPLATE = "Privilege named '{}' found in DB, but was not specified in SillySettings"
            PRIVILEGE_NOT_FOUND_TEMPLATE = "Privilege named '{}' is unknown."
            USER_WITH_UNKNOWN_PRIVILEGE = "User {} has an unknown privilege '{}'."
            CUSTOM_CONTROLS_FLAG_INCOMPATIBLE = (
                "CUSTOM_CONTROLS flag is incompatible with any others"
            )
