import unittest
from core.data.registry.session import Registrable
from abc import abstractmethod, ABC

K = "K"
V = "V"
U = 0
U1 = 1
U2 = 2
V1 = "V1"
V2 = "V2"
K1 = "K1"
K2 = "K2"


class RegistryTests(unittest.TestCase, ABC):
    _registry: Registrable

    @abstractmethod
    def setUp(self):
        raise NotImplementedError()

    def test_initial_state_global(self):
        exception: bool = False

        try:
            self._registry.get_value(K)
        except Exception as e:
            exception = True

        self.assertTrue(exception, True)

    def test_initial_state_local(self):
        exception: bool = False

        try:
            self._registry.get_value((K, U))
        except Exception as e:
            exception = True

        self.assertTrue(exception, True)

    def test_key_addition_1(self):
        self._registry.establish_key(K)
        self.assertEqual(self._registry.get_value(K), None)

    def test_key_addition_2(self):
        self._registry.establish_key(K)
        self.assertEqual(self._registry.get_value((K, U)), None)

    def test_key_default_value_addition_1(self):
        self._registry.establish_key(K, V)
        self.assertEqual(self._registry.get_value(K), V)

    def test_key_default_value_addition_2(self):
        self._registry.establish_key(K)
        self.assertEqual(self._registry.get_value((K, U)), None)

    def test_users_1(self):
        self._registry.establish_key(K, None)
        self._registry.set_value(K, V1)
        self._registry.set_value((K, U2), V2)
        self.assertEqual(self._registry.get_value((K, U2)), V2)

    def test_users_2(self):
        self._registry.establish_key(K, None)
        self._registry.set_value(K, V1)
        self._registry.set_value((K, U2), None)
        self.assertEqual(self._registry.get_value((K, U2)), V1)

    def test_default_1(self):
        self._registry.establish_key(K, V)
        self._registry.set_value((K, U1), V1)
        self._registry.set_value((K, U2), V2)

        self._registry.establish_key(K, self._registry.get_value(K))
        self.assertEqual(self._registry.get_value((K, U1)), V)

    def test_default_2(self):
        self._registry.establish_key(K, V)
        self._registry.set_value((K, U1), V1)
        self._registry.set_value((K, U2), V2)

        self._registry.establish_key(K, self._registry.get_value(K))
        self.assertEqual(self._registry.get_value((K, U2)), V)

    def test_key_removal_1(self):
        exception: bool = False

        try:
            self._registry.establish_key(K, V)
            self._registry.set_value((K, U1), V1)
            self._registry.set_value((K, U2), V2)
            self._registry.remove_key(K)

            self._registry.get_value(K)
        except Exception as e:
            exception = True

        self.assertTrue(exception, True)


    def test_key_removal_2(self):
        exception: bool = False

        self._registry.establish_key(K, V)
        self._registry.set_value((K, U1), V1)
        self._registry.set_value((K, U2), V2)
        self._registry.remove_key(K)

        try:
            self._registry.get_value((K, U1))

        except KeyError as e:
            exception = True

        self.assertTrue(exception, True)

    def test_key_removal_3(self):
        exception: bool = False

        self._registry.establish_key(K, V)
        self._registry.set_value((K, U1), V1)
        self._registry.set_value((K, U2), V2)
        self._registry.remove_key(K)

        try:
            self._registry.get_value((K, U2))
        except KeyError as e:
            exception = True

        self.assertTrue(exception, True)

    def test_reset_1(self):
        exception: bool = False

        self._registry.establish_key(K, V)
        self._registry.set_value((K, U1), V1)
        self._registry.set_value((K, U2), V2)

        self._registry.reset()

        try:
            self._registry.get_value((K, U1))

        except KeyError as e:
            exception = True

        self.assertTrue(exception, True)

    def test_reset_2(self):
        exception: bool = False

        self._registry.establish_key(K, V)
        self._registry.set_value((K, U1), V1)
        self._registry.set_value((K, U2), V2)

        self._registry.reset()

        try:
            self._registry.get_value(K)

        except KeyError as e:
            exception = True

        self.assertTrue(exception, True)

    def test_user_reset_0(self):
        self._registry.establish_key(K1, K1)
        self._registry.establish_key(K2, K1)

        self._registry.set_value((K1, U1), V1)
        self._registry.set_value((K2, U1), V2)

        v = self._registry.get_value((K1, U1))

        self.assertTrue(v, V1)

    def test_user_reset_1(self):
        self._registry.establish_key(K1, K1)
        self._registry.establish_key(K2, K1)

        self._registry.set_value((K1, U1), V1)
        self._registry.set_value((K2, U1), V2)

        self._registry.reset_user(U1)
        v = self._registry.get_value((K1, U1))

        self.assertTrue(v, K1)

    def test_user_reset_2(self):
        self._registry.establish_key(K1, K1)
        self._registry.establish_key(K2, K1)

        self._registry.set_value((K1, U1), V1)
        self._registry.set_value((K2, U1), V2)

        self._registry.reset_user(U1)
        v = self._registry.get_value((K2, U1))

        self.assertTrue(v, K2)

    def test_null(self):
        self._registry.establish_key(K1, None)
        self.assertEqual(self._registry.get_value(K1), None)

















