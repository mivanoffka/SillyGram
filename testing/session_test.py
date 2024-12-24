from sillygram.data.registry.session import SessionRegistry
from .registry_test import RegistryTests


class SessionTests(RegistryTests):
    def setUp(self):
        self._registry = SessionRegistry()
