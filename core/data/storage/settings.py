from typing import Optional

from .labels import SillyLabels


class SillySettings:
    _labels: SillyLabels
    _skip_updates: bool = True

    @property
    def labels(self):
        return self._labels

    @property
    def skip_updates(self):
        return self._skip_updates

    def __init__(self, labels: Optional[SillyLabels] = None, skip_updates: bool = True):
        self._skip_updates = skip_updates
        self._labels = labels if labels else SillyLabels()
