"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import unittest
import pydarkstar.logutils
import pydarkstar.tables.auctionhouse

pydarkstar.logutils.setDebug()

class TestAuctionHouse(unittest.TestCase):
    def test_init(self):
        row = pydarkstar.tables.auctionhouse.AuctionHouse()
        pydarkstar.logutils.logging.debug(row)

if __name__ == '__main__':
    unittest.main()