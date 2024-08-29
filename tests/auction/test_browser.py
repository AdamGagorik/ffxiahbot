import logging

from ffxiahbot.auction.browser import Browser
from tests import sqltest


class TestCase01(sqltest.TestSQL):
    def setUp(self):
        super().setUp()
        self.ob = Browser(self.db, fail=True)

    def test_count(self):
        self.ob.count()

    def test_getStock(self):
        logging.debug("stock = %s", self.ob.get_stock(1, 0))

    def test_getPrice(self):
        logging.debug("price = %s", self.ob.get_price(1, 0))
