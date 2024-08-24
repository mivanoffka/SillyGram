from typing import Optional

from .labels import SillyLabels


class SillySettings:
    _labels: SillyLabels
    _skip_updates: bool = True
    _log_to_console: bool = False

    @property
    def labels(self):
        return self._labels

    @property
    def skip_updates(self):
        return self._skip_updates

    @property
    def log_to_console(self):
        return self._log_to_console

    def __init__(self, labels: Optional[SillyLabels] = None, skip_updates: bool = True, log_to_console: bool = False):
        self._skip_updates = skip_updates
        self._log_to_console = log_to_console
        self._labels = labels if labels else SillyLabels()
