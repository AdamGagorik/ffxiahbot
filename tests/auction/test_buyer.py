from ffxiahbot.auction.buyer import Buyer
from tests import sqltest


class TestCase01(sqltest.TestSQL):
    def setUp(self):
        super().setUp()
        self.ob = Buyer(self.db, fail=True)
