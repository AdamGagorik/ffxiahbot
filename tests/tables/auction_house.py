"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import unittest
import pydarkstar.logutils
import pydarkstar.tables.auction_house

pydarkstar.logutils.setDebug()

class TestAuctionHouse(unittest.TestCase):
    def test_init(self):
        row = pydarkstar.tables.auction_house.AuctionHouse()
        pydarkstar.logutils.logging.debug(row)

if __name__ == '__main__':
    unittest.main()