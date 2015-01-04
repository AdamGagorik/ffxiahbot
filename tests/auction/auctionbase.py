"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import unittest

import pydarkstar.logutils
import pydarkstar.database
import pydarkstar.auction.auctionbase
import pydarkstar.rc

pydarkstar.logutils.setDebug()

class TestAuctionBase(unittest.TestCase):
    def setUp(self):
        self.db = pydarkstar.database.Database.pymysql(**pydarkstar.rc.sql)

    def test_init(self):
        pydarkstar.auction.auctionbase.AuctionBase(self.db)

if __name__ == '__main__':
    unittest.main()