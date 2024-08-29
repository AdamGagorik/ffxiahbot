import unittest

from ffxiahbot.tables.auctionhouse import AuctionHouse


class TestCase01(unittest.TestCase):
    def setUp(self):
        self.ah = AuctionHouse()

    def test_init(self):
        pass

    def test_str(self):
        str(self.ah)
