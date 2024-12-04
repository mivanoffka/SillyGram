from ..ui import ActionButton, SillyPage, NavigationButton
from ..data import SillyDefaults
from ..manager import SillyManager
from ..user import SillyUser


@SillyManager.admin_only
async def _not_implemented(manager: SillyManager, user: SillyUser):
    await manager.show_message(user, SillyDefaults.Configurator.NOT_IMPLEMENTED_TEXT)


@SillyManager.admin_only
async def _on_stats_button_clicked(manager: SillyManager, user: SillyUser):
    await manager.show_message(user, manager.stats)


configuration_page = SillyPage(
    name=SillyDefaults.Names.CONFIGURE_PAGE,
    text=SillyDefaults.Configurator.ROOT_PAGE_TEXT,
    buttons=(
        (
            ActionButton(
                SillyDefaults.Configurator.STATS_BUTTON_TEXT, _on_stats_button_clicked
            ),
        ),
        (
            NavigationButton(
                SillyDefaults.Configurator.ADMINS_BUTTON_TEXT,
                SillyDefaults.Configurator.AdminsPage.NAME,
            ),
            NavigationButton(
                SillyDefaults.Configurator.BANNED_BUTTON_TEXT,
                SillyDefaults.Configurator.BannedPage.NAME,
            ),
        ),
        (
            NavigationButton(
                SillyDefaults.Configurator.HOME_BUTTON_TEXT,
                SillyDefaults.Names.HOME_PAGE,
            ),
        ),
    ),
)
