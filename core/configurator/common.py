from ..manager import SillyManager
from ..user import SillyUser
from ..data import SillyDefaults


async def get_user(manager: SillyManager, user: SillyUser):
    user_to_promote: SillyUser
    input_str = "?"
    try:
        input_str = await manager.get_input(user, SillyDefaults.Configurator.USER_ID_INPUT_PROMPT)
        user_to_promote = manager.users.get(input_str)
    except Exception as e:
        await manager.show_message(user, SillyDefaults.Configurator.ERROR_MESSAGE_TEMPLATE.format(
            SillyDefaults.Configurator.USER_NOT_REGISTERED_ERROR_TEMPLATE.format(input_str)
        ))
        return None

    return user_to_promote
