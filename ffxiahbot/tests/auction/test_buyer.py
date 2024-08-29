import unittest

from ffxiahbot.tests import sqltest

import_error = False
try:
    from ffxiahbot.auction.buyer import Buyer
except ImportError:
    import_error = True
    Buyer = None


class TestCase00(unittest.TestCase):
    def test_import(self):
        self.assertFalse(import_error)


class TestCase01(sqltest.TestSQL):
    def setUp(self):
        super().setUp()
        if import_error:
            self.skipTest("ImportError")
        else:
            self.ob = Buyer(self.db, fail=True)
