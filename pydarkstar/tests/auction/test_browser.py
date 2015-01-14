import unittest
import logging
logging.getLogger().setLevel(logging.DEBUG)

from ...auction.browser import Browser
from ...database import Database
from ...rc import sql

class TestCase(unittest.TestCase):
    def setUp(self):
        self.db = Database.pymysql(**sql)
        self.ob = Browser(self.db, fail=True)

    def test_init(self):
        pass

    def test_count(self):
        self.ob.count()

    def test_getStock(self):
        logging.debug('stock = %s', self.ob.getStock(1, 0))

    def test_getPrice(self):
        logging.debug('price = %s', self.ob.getPrice(1, 0))