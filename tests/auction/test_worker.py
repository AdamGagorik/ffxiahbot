from ffxiahbot.auction.worker import Worker
from tests import sqltest


class TestCase01(sqltest.TestSQL):
    def setUp(self):
        super().setUp()
        self.ob = Worker(self.db, fail=True)
