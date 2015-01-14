import unittest
import logging
logging.getLogger().setLevel(logging.DEBUG)

from ...auction.cleaner import Cleaner
from ...database import Database
from ...rc import sql

class TestCase(unittest.TestCase):
    def setUp(self):
        self.db = Database.pymysql(**sql)
        self.ob = Cleaner(self.db, fail=True)

    def test_init(self):
        pass

    def test_clear(self):
        with self.assertRaises(RuntimeError):
            self.ob.clear(seller=1.1)