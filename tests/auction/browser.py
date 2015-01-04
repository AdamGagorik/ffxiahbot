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

class TestBrowser(unittest.TestCase):
    def setUp(self):
        self.db = pydarkstar.database.Database.pymysql(**pydarkstar.rc.sql)

    def test_init(self):
        pydarkstar.auctionhouse.browser.Browser(self.db)

    def test_count(self):
        browser = pydarkstar.auctionhouse.browser.Browser(self.db)
        browser.count()

    def test_getStock(self):
        browser = pydarkstar.auctionhouse.browser.Browser(self.db)
        logging.debug('stock = %s', browser.getStock(1, 0))

    def test_getPrice(self):
        browser = pydarkstar.auctionhouse.browser.Browser(self.db)
        logging.debug('price = %s', browser.getPrice(1, 0))

if __name__ == '__main__':
    unittest.main()