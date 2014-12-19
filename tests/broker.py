"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import unittest
import pydarkstar.logutils
import pydarkstar.database
import pydarkstar.broker
import pydarkstar.rc

pydarkstar.logutils.setDebug()

class TestDarkObject(unittest.TestCase):
    def setUp(self):
        self.db = pydarkstar.database.Database.pymysql(**pydarkstar.rc.sql)

    def test_init(self):
        pydarkstar.broker.Broker(self.db)

if __name__ == '__main__':
    unittest.main()