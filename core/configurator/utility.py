from typing import Optional

from ..data import SillyDefaults, SillyUser


async def get_user_name_or_id(manager, event, prompt: Optional[str]) -> SillyUser:
    prompt = prompt if prompt else SillyDefaults.Configurator.USER_ID_INPUT_PROMPT
    uid_or_name = await manager.get_input(event.user, prompt)

    user = manager.get_user(uid_or_name)
    if user is None:
        try:
            uid = int(uid_or_name)
            user = manager.get_user(uid)
            if user is None:
                raise Exception()
        except Exception as e:
            raise KeyError(SillyDefaults.Configurator.USER_NOT_REGISTERED_ERROR_TEMPLATE.format(uid_or_name))
    else:
        return user
