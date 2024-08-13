from typing import Optional

from .labels import SillyLabels


class SillySettings:
    _labels: SillyLabels

    @property
    def labels(self):
        return self._labels

    def __init__(self, labels: Optional[SillyLabels] = None):
        self._labels = labels if labels else SillyLabels()
