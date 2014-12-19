"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import unittest
import pydarkstar.logutils
import pydarkstar.database
import pydarkstar.rc

pydarkstar.logutils.setDebug()

class TestDatabase(unittest.TestCase):
    def test_pymysql(self):
        pydarkstar.database.Database.pymysql(**pydarkstar.rc.sql)

if __name__ == '__main__':
    unittest.main()