import logging
import unittest

from ffxiahbot.tests import sqltest

import_error = False
try:
    from ffxiahbot.auction.browser import Browser
except ImportError:
    import_error = True
    Browser = None


class TestCase00(unittest.TestCase):
    def test_import(self):
        self.assertFalse(import_error)


class TestCase01(sqltest.TestSQL):
    def setUp(self):
        super().setUp()
        if import_error:
            self.skipTest("ImportError")
        else:
            self.ob = Browser(self.db, fail=True)

    def test_count(self):
        self.ob.count()

    def test_getStock(self):
        logging.debug("stock = %s", self.ob.get_stock(1, 0))

    def test_getPrice(self):
        logging.debug("price = %s", self.ob.get_price(1, 0))
