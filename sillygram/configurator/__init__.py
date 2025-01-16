from .configurator import configuration_page as _configuration_page
from .banned import banned_page as _banned_page
from .communication import communication_page as _communication_page

configurator = (_configuration_page, _banned_page, _communication_page)
