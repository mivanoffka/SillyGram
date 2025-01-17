from .options import options_page as _options_page
from .banned import banned_page as _banned_page
from .communication import communication_page as _communication_page, broadcast_status_page as _broadcast_status_page

options_pages = (_options_page, _banned_page, _communication_page, _broadcast_status_page)
