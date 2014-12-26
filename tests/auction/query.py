"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import unittest

import pydarkstar.logutils
import pydarkstar.database
import pydarkstar.auction.query
import pydarkstar.rc

pydarkstar.logutils.setDebug()

class TestQuery(unittest.TestCase):
    def setUp(self):
        self.db = pydarkstar.database.Database.pymysql(**pydarkstar.rc.sql)

    def test_getStock(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()