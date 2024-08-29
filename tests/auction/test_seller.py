from ffxiahbot.auction.seller import Seller
from tests import sqltest


class TestCase01(sqltest.TestSQL):
    def setUp(self):
        super().setUp()
        self.ob = Seller(self.db, fail=True)
