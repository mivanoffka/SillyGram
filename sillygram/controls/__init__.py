from .root import root_controls_page as _root_controls_page
from .banned import banned_page as _banned_page
from .communication import communication_page as _communication_page, broadcast_status_page as _broadcast_status_page

controls_pages = (_root_controls_page, _banned_page, _communication_page, _broadcast_status_page)
