"""
TestCase for SQL.
"""
from pydarkstar.database import Database
import sqlalchemy.exc
import unittest
import logging

# sql database parameters
mysql_params = dict(
    hostname='127.0.0.1',
    database='dspdb',
    username='root',
    password='cisco',
)


class TestSQL(unittest.TestCase):
    def setUp(self):
        self.db = Database.pymysql(**mysql_params)
        try:
            self.db.engine.connect()
        except sqlalchemy.exc.OperationalError:
            logging.exception('SQL')
            self.skipTest('OperationalError')


if __name__ == '__main__':
    pass
