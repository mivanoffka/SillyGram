from tkinter import E
from typing import Optional
from ..manager import SillyManager
from ..user import SillyUser
from ..data import SillyDefaults


async def get_user(manager: SillyManager, user: SillyUser) -> Optional[SillyUser]:
    user_to_promote: Optional[SillyUser] = None
    input_str = "?"
    try:
        input_str = await manager.get_input(user, SillyDefaults.Configurator.USER_ID_INPUT_PROMPT)
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
        await manager.show_message(user, SillyDefaults.Configurator.ERROR_MESSAGE_TEMPLATE.format(
            SillyDefaults.Configurator.USER_NOT_REGISTERED_ERROR_TEMPLATE.format(e)
        ))
        return None

    return user_to_promote
