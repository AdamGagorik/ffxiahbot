import unittest

from .. import sqltest

import_error = False
try:
    from ...auction.cleaner import Cleaner
except ImportError:
    import_error = True
    Cleaner = None


class TestCase00(unittest.TestCase):
    def test_import(self):
        self.assertFalse(import_error)


class TestCase01(sqltest.TestSQL):
    def setUp(self):
        super(TestCase01, self).setUp()
        if import_error:
            self.skipTest('ImportError')
        else:
            self.ob = Cleaner(self.db, fail=True)

    def test_clear(self):
        with self.assertRaises(RuntimeError):
            self.ob.clear(seller=1.1)
