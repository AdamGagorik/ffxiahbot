"""
TestCase for SQL.
"""

import logging
import unittest

import sqlalchemy.exc

from ffxiahbot.database import Database

# sql database parameters
mysql_params = {
    "hostname": "127.0.0.1",
    "database": "dspdb",
    "username": "root",
    "password": "cisco",
}


class TestSQL(unittest.TestCase):
    def setUp(self):
        self.db = Database.pymysql(**mysql_params)
        try:
            self.db.engine.connect()
        except sqlalchemy.exc.OperationalError:
            logging.exception("SQL")
            self.skipTest("OperationalError")


if __name__ == "__main__":
    pass
