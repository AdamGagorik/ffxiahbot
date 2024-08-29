import unittest

import_error = False
try:
    from ffxiahbot.tables.auctionhouse import AuctionHouse
except ImportError:
    import_error = True
    AuctionHouse = None


class TestCase00(unittest.TestCase):
    def test_import(self):
        self.assertFalse(import_error)


class TestCase01(unittest.TestCase):
    def setUp(self):
        self.ah = AuctionHouse()

    def test_init(self):
        pass

    def test_str(self):
        str(self.ah)
