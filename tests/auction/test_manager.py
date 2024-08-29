from ffxiahbot.auction.manager import Manager
from tests import sqltest


class TestCase01(sqltest.TestSQL):
    def setUp(self):
        super().setUp()
        self.ob = Manager(self.db, fail=True)
