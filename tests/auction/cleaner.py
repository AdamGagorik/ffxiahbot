"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import unittest

import pydarkstar.logutils
import pydarkstar.database
import pydarkstar.auction.cleaner
import pydarkstar.rc

pydarkstar.logutils.setDebug()

class TestCleaner(unittest.TestCase):
    def setUp(self):
        self.db = pydarkstar.database.Database.pymysql(**pydarkstar.rc.sql)

    def test_init(self):
        pydarkstar.auction.cleaner.Cleaner(self.db)

    def test_clear(self):
        cleaner = pydarkstar.auction.cleaner.Cleaner(self.db, fail=True)
        with self.assertRaises(RuntimeError):
            cleaner.clear(seller=1.1)

if __name__ == '__main__':
    unittest.main()