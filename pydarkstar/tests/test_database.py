import unittest
import logging
logging.getLogger().setLevel(logging.DEBUG)

from ..database import Database
from ..rc import sql
import sqlalchemy.exc

class TestCase(unittest.TestCase):
    def setUp(self):
        self.db = Database.pymysql(**sql)

    def test_init(self):
        pass

    def test_scoped_session1(self):
        with self.assertRaises(RuntimeError):
            with self.db.scoped_session(rollback=True, fail=True):
                raise sqlalchemy.exc.SQLAlchemyError('IGNORE THIS ERROR')

    def test_scoped_session2(self):
        with self.db.scoped_session(rollback=True, fail=False):
            raise sqlalchemy.exc.SQLAlchemyError('IGNORE THIS ERROR')

if __name__ == '__main__':
    unittest.main()