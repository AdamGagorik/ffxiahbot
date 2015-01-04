"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import unittest
import pydarkstar.logutils
import pydarkstar.database
import pydarkstar.rc
import sqlalchemy.exc

pydarkstar.logutils.setDebug()

class TestDatabase(unittest.TestCase):
    def test_pymysql(self):
        pydarkstar.database.Database.pymysql(**pydarkstar.rc.sql)

    def test_scoped_session1(self):
        db = pydarkstar.database.Database.pymysql(**pydarkstar.rc.sql)
        with self.assertRaises(RuntimeError):
            with db.scoped_session(rollback=True, fail=True):
                raise sqlalchemy.exc.SQLAlchemyError('DATABASE TEST : IGNORE THIS ERROR')

    def test_scoped_session2(self):
        db = pydarkstar.database.Database.pymysql(**pydarkstar.rc.sql)
        with db.scoped_session(rollback=True, fail=False):
            raise sqlalchemy.exc.SQLAlchemyError('DATABASE TEST : IGNORE THIS ERROR')

if __name__ == '__main__':
    unittest.main()