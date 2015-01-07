"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import unittest

import pydarkstar.logutils
import pydarkstar.database
import pydarkstar.auctionhouse.browser
import pydarkstar.rc
import logging

pydarkstar.logutils.setDebug()

class TestCase(unittest.TestCase):
    def setUp(self):
        self.db = pydarkstar.database.Database.pymysql(**pydarkstar.rc.sql)
        self.ob = pydarkstar.auctionhouse.browser.Browser(self.db, fail=True)

    def test_init(self):
        pass

    def test_count(self):
        self.ob.count()

    def test_getStock(self):
        logging.debug('stock = %s', self.ob.getStock(1, 0))

    def test_getPrice(self):
        logging.debug('price = %s', self.ob.getPrice(1, 0))

if __name__ == '__main__':
    unittest.main()