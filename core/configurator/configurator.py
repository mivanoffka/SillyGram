from ..ui import ActionButton, SillyPage, NavigationButton
from ..data import SillyDefaults
from ..manager import SillyManager
from ..user import SillyUser


@SillyManager.admin_only
async def _not_implemented(manager: SillyManager, user: SillyUser):
    await manager.show_message(user, SillyDefaults.Configurator.NOT_IMPLEMENTED_TEXT)


configuration_page = SillyPage(name=SillyDefaults.Names.CONFIGURE_PAGE,
                               text=SillyDefaults.Configurator.ROOT_PAGE_TEXT,
                               buttons=(
                                   (NavigationButton(SillyDefaults.Configurator.ADMINS_BUTTON_TEXT,
                                                     SillyDefaults.Configurator.AdminsPage.NAME),
                                    NavigationButton(SillyDefaults.Configurator.BANNED_BUTTON_TEXT,
                                                     SillyDefaults.Configurator.BannedPage.NAME)),
                                    ActionButton(SillyDefaults.Configurator.STATS_BUTTON_TEXT,
                                                    _not_implemented),
                                   (NavigationButton(SillyDefaults.Configurator.HOME_BUTTON_TEXT,
                                                     SillyDefaults.Names.HOME_PAGE),
                                    ActionButton(SillyDefaults.Configurator.REGISTRY_BUTTON_TEXT,
                                                     _not_implemented),
                                    ActionButton(SillyDefaults.Configurator.RESET_BUTTON_TEXT,
                                                 _not_implemented))
                               ))
