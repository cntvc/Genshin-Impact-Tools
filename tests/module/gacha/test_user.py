import unittest

from genshin.module.user import user


class TestUser(unittest.TestCase):
    def test_set_uid(self):
        user.set_uid("123456788")
        self.assertIs(user.get_uid(), "123456788")

        self.assertFalse(user.set_uid("1"))

        user.reset()
        self.assertEqual(user.get_uid(), "")

    def test_area(self):
        user.set_uid("512345678")
        self.assertEqual(user.get_area(), "cn")
        user.set_uid("612345678")
        self.assertEqual("global", user.get_area())
