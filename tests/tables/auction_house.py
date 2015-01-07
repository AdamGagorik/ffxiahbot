import unittest
import pydarkstar.logutils
import pydarkstar.tables.auctionhouse

pydarkstar.logutils.setDebug()

class TestCase(unittest.TestCase):
    def test_init(self):
        row = pydarkstar.tables.auctionhouse.AuctionHouse()
        pydarkstar.logutils.logging.debug(row)

if __name__ == '__main__':
    unittest.main()