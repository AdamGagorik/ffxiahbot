"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import unittest

import pydarkstar.logutils
import pydarkstar.database
import pydarkstar.auction.buyer
import pydarkstar.rc

pydarkstar.logutils.setDebug()

class TestCase(unittest.TestCase):
    def setUp(self):
        self.db = pydarkstar.database.Database.pymysql(**pydarkstar.rc.sql)
        self.ob = pydarkstar.auction.buyer.Buyer(self.db, fail=True)

    def test_init(self):
        pass

if __name__ == '__main__':
    unittest.main()