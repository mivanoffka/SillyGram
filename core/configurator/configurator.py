from ..ui import ActionButton, SillyPage, NavigationButton
from ..data import SillyDefaults
from ..management import SillyManager


configuration_page = SillyPage(name=SillyDefaults.Names.CONFIGURE_PAGE,
                               text=SillyDefaults.Configurator.ROOT_PAGE_TEXT,
                               buttons=(
                                   (NavigationButton(SillyDefaults.Configurator.ADMINS_BUTTON_TEXT,
                                                     SillyDefaults.Configurator.AdminsPage.NAME),
                                    NavigationButton(SillyDefaults.Configurator.BANNED_BUTTON_TEXT,
                                                     SillyDefaults.Configurator.BannedPage.NAME)),
                                   NavigationButton(SillyDefaults.Configurator.STATS_BUTTON_TEXT,
                                                    SillyDefaults.Configurator.StatsPage.NAME),
                                   (NavigationButton(SillyDefaults.Configurator.HOME_BUTTON_TEXT,
                                                     SillyDefaults.Names.HOME_PAGE),
                                    NavigationButton(SillyDefaults.Configurator.REGISTRY_BUTTON_TEXT,
                                                     SillyDefaults.Configurator.RegistryPage.NAME),
                                    ActionButton(SillyDefaults.Configurator.RESET_BUTTON_TEXT,
                                                 SillyDefaults.Configurator.AdminsPage.NAME))
                               ))
