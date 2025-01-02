from ..ui import ActionSillyButton, SillyPage, NavigationSillyButton
from ..data import SillyDefaults
from ..manager import SillyManager
from ..events import SillyEvent


@SillyManager.admin_only
async def _not_implemented(manager: SillyManager, event: SillyEvent):
    await manager.show_popup(event.user, SillyDefaults.Configurator.NOT_IMPLEMENTED_TEXT)


@SillyManager.admin_only
async def _on_stats_button_clicked(manager: SillyManager, event: SillyEvent):
    await manager.show_popup(event.user, manager.stats)


configuration_page = SillyPage(
    name=SillyDefaults.Names.CONFIGURE_PAGE,
    text=SillyDefaults.Configurator.ROOT_PAGE_TEXT,
    buttons=(
        (
            ActionSillyButton(
                SillyDefaults.Configurator.STATS_BUTTON_TEXT, _on_stats_button_clicked
            ),
        ),
        (
            NavigationSillyButton(
                SillyDefaults.Configurator.ADMINS_BUTTON_TEXT,
                SillyDefaults.Configurator.AdminsPage.NAME,
            ),
            NavigationSillyButton(
                SillyDefaults.Configurator.BANNED_BUTTON_TEXT,
                SillyDefaults.Configurator.BannedPage.NAME,
            ),
        ),
        (
            NavigationSillyButton(
                SillyDefaults.Configurator.HOME_BUTTON_TEXT,
                SillyDefaults.Names.HOME_PAGE,
            ),
        ),
    ),
)
