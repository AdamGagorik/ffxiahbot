import unittest

from .. import sqltest

import_error = False
try:
    from ...auction.seller import Seller
except ImportError:
    import_error = True
    Seller = None


class TestCase00(unittest.TestCase):
    def test_import(self):
        self.assertFalse(import_error)


class TestCase01(sqltest.TestSQL):
    def setUp(self):
        super(TestCase01, self).setUp()
        if import_error:
            self.skipTest('ImportError')
        else:
            self.ob = Seller(self.db, fail=True)
