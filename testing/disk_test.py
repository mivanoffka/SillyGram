from core.data.registry.disk import DiskRegistry
from .registry_test import RegistryTests, K, V, U1, V1, U2, V2
from utility import SillyDB
from core.data.orm import DECLARATIVE_BASE


class DiskTests(RegistryTests):
    def setUp(self):
        self._registry = DiskRegistry(SillyDB("test", DECLARATIVE_BASE))
        self._registry.reset()
