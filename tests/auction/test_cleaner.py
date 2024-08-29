from ffxiahbot.auction.cleaner import Cleaner
from tests import sqltest


class TestCase01(sqltest.TestSQL):
    def setUp(self):
        super().setUp()
        self.ob = Cleaner(self.db, fail=True)

    def test_clear(self):
        with self.assertRaises(RuntimeError):
            self.ob.clear(seller=1.1)
