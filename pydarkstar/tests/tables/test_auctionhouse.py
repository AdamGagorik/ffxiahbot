import unittest
import logging

logging.getLogger().setLevel(logging.DEBUG)

from ...tables.auctionhouse import AuctionHouse


class TestCase(unittest.TestCase):
    def setUp(self):
        self.ah = AuctionHouse()

    def test_init(self):
        pass

    def test_str(self):
        s = str(self.ah)
        logging.debug(s)
