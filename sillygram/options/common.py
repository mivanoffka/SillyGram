from typing import Optional
from ..manager import SillyManager
from ..user import SillyUser
from ..data import SillyDefaults
from ..events import SillyEvent


async def get_user(manager: SillyManager, event: SillyEvent) -> Optional[SillyUser]:
    user_to_promote: Optional[SillyUser] = None
    input_str = "?"
    try:
        input_str = await manager.get_input(event.user, SillyDefaults.Options.USER_ID_INPUT_PROMPT)
        if not input_str:
            return None
        user_to_promote = manager.users.get(input_str)

        if not user_to_promote:
            try:
                uid = int(input_str)
            except Exception:
                raise Exception(input_str)
            user_to_promote = manager.users.get(uid)

            if not user_to_promote:
                raise Exception(input_str)

    except Exception as e:
        await manager.show_popup(event.user, SillyDefaults.Options.ERROR_MESSAGE_TEMPLATE.format(
            SillyDefaults.Options.USER_NOT_REGISTERED_ERROR_TEMPLATE.format(e)
        ))
        return None

    return user_to_promote
