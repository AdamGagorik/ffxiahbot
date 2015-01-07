import unittest

import pydarkstar.logutils
import pydarkstar.database
import pydarkstar.auction.cleaner
import pydarkstar.rc

pydarkstar.logutils.setDebug()

class TestCase(unittest.TestCase):
    def setUp(self):
        self.db = pydarkstar.database.Database.pymysql(**pydarkstar.rc.sql)
        self.ob = pydarkstar.auction.cleaner.Cleaner(self.db, fail=True)

    def test_init(self):
        pass

    def test_clear(self):
        with self.assertRaises(RuntimeError):
            self.ob.clear(seller=1.1)

if __name__ == '__main__':
    unittest.main()