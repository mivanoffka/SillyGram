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

    # region Commands
    @dataclass(frozen=True)
    class Commands:
        START = "start"
        HOME = "home"











