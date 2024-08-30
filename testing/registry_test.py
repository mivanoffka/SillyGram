import unittest
from core.data.registry.session import SessionRegistry

K = "K"
V = "V"
U = 0
U1 = 1
U2 = 2
V1 = "V1"
V2 = "V2"


class RegistryTests(unittest.TestCase):
    _registry: SessionRegistry

    def test_initial_state_global(self):
        self._registry = SessionRegistry()
        exception: bool = False

        try:
            self._registry[K]
        except Exception as e:
            exception = True
            
        self.assertTrue(exception, True)

    def test_initial_state_local(self):
        self._registry = SessionRegistry()
        exception: bool = False

        try:
            self._registry[K, U]
        except Exception as e:
            exception = True

        self.assertTrue(exception, True)

    def test_key_addition_1(self):
        self._registry = SessionRegistry()
        self._registry.establish_key(K)
        self.assertEqual(self._registry.get_value(K), None)

    def test_key_addition_2(self):
        self._registry = SessionRegistry()
        self._registry.establish_key(K)
        self.assertEqual(self._registry.get_value((K, U)), None)

    def test_key_default_value_addition_1(self):
        self._registry = SessionRegistry()
        self._registry.establish_key(K, V)
        self.assertEqual(self._registry.get_value(K), V)

    def test_key_default_value_addition_2(self):
        self._registry = SessionRegistry()
        self._registry.establish_key(K)
        self.assertEqual(self._registry.get_value((K, U)), None)

    def test_users_1(self):
        self._registry = SessionRegistry()
        self._registry.establish_key(K, None)
        self._registry.set_value(K, V1)
        self._registry.set_value((K, U2), V2)
        self.assertEqual(self._registry.get_value((K, U2)), V2)

    def test_users_2(self):
        self._registry = SessionRegistry()
        self._registry.establish_key(K, None)
        self._registry.set_value(K, V1)
        self._registry.set_value((K, U2), None)
        self.assertEqual(self._registry.get_value((K, U2)), V1)

    def test_default_1(self):
        registry = SessionRegistry()
        registry.establish_key(K, V)
        registry.set_value((K, U1), V1)
        registry.set_value((K, U2), V2)

        registry.establish_key(K, registry.get_value(K))
        self.assertEqual(registry.get_value((K, U1)), V)

    def test_default_2(self):
        registry = SessionRegistry()
        registry.establish_key(K, V)
        registry.set_value((K, U1), V1)
        registry.set_value((K, U2), V2)

        registry.establish_key(K, registry.get_value(K))
        self.assertEqual(registry.get_value((K, U2)), V)

    def test_key_removal_1(self):
        registry = SessionRegistry()
        exception: bool = False

        try:
            registry.establish_key(K, V)
            registry.set_value((K, U1), V1)
            registry.set_value((K, U2), V2)
            registry.remove_key(K)

            registry.get_value(K)
        except Exception as e:
            exception = True

        self.assertTrue(exception, True)


    def test_key_removal_2(self):
        registry = SessionRegistry()
        exception: bool = False

        registry.establish_key(K, V)
        registry.set_value((K, U1), V1)
        registry.set_value((K, U2), V2)
        registry.remove_key(K)

        try:
            registry.get_value((K, U1))

        except KeyError as e:
            exception = True

        self.assertTrue(exception, True)

    def test_key_removal_3(self):
        registry = SessionRegistry()
        exception: bool = False

        registry.establish_key(K, V)
        registry.set_value((K, U1), V1)
        registry.set_value((K, U2), V2)
        registry.remove_key(K)

        try:
            registry.get_value((K, U2))
        except KeyError as e:
            exception = True

        self.assertTrue(exception, True)
















