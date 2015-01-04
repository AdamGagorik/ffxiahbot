"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import unittest

import pydarkstar.logutils
import pydarkstar.database
import pydarkstar.auctionhouse.buyer
import pydarkstar.rc

pydarkstar.logutils.setDebug()

class TestBuyer(unittest.TestCase):
    def setUp(self):
        self.db = pydarkstar.database.Database.pymysql(**pydarkstar.rc.sql)

    def test_init(self):
        pydarkstar.auctionhouse.buyer.Buyer(self.db)

if __name__ == '__main__':
    unittest.main()