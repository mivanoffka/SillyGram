from __future__ import annotations

from typing import Optional, Sequence, Callable, Awaitable, TYPE_CHECKING, Tuple

from .defaults import SillyDefaults

if TYPE_CHECKING:
    from ...manager import SillyManager
    from ...activities import SillyRegularActivity
    from ...privelege import SillyPrivelege

from .labels import SillyLabels


class SillySettings:
    _labels: SillyLabels
    _skip_updates: bool = True
    _log_to_console: bool = False

    _regular_activities: Optional[Sequence[SillyRegularActivity]] = None
    _on_startup: Optional[Callable[[SillyManager], Awaitable[None]]] = None
    _on_shutdown: Optional[Callable[[SillyManager], Awaitable[None]]] = None

    _priveleges: Optional[Tuple[SillyPrivelege, ...]] = None

    @property
    def labels(self):
        return self._labels

    @property
    def skip_updates(self):
        return self._skip_updates

    @property
    def log_to_console(self):
        return self._log_to_console

    @property
    def regular_activities(self):
        return self._regular_activities

    @property
    def on_startup(self):
        return self._on_startup

    @property
    def on_shutdown(self):
        return self._on_shutdown

    @property
    def priveleges(self):
        return self._priveleges

    @property
    def master_users(self):
        return self._master_users

    def __init__(
        self,
        labels: Optional[SillyLabels] = None,
        regular_activities: Optional[Sequence[SillyRegularActivity]] = None,
        on_startup: Optional[Callable[[SillyManager], Awaitable[None]]] = None,
        on_shutdown: Optional[Callable[[SillyManager], Awaitable[None]]] = None,
        skip_updates: bool = True,
        log_to_console: bool = False,
        priveleges: Optional[Sequence[SillyPrivelege]] = None,
        master_users: Optional[Sequence[int|str]] = None,
    ):
        self._skip_updates = skip_updates
        self._log_to_console = log_to_console
        self._labels = labels if labels else SillyLabels()

        self._regular_activities = regular_activities
        self._on_startup = on_startup
        self._on_shutdown = on_shutdown

        self._priveleges = tuple(priveleges) if priveleges else None
        self._master_users = tuple(master_users) if master_users else None
