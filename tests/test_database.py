import sqlalchemy.exc

from tests import sqltest


class TestCase01(sqltest.TestSQL):
    def test_scoped_session1(self):
        with self.assertRaises(RuntimeError), self.db.scoped_session(rollback=True, fail=True):
            raise sqlalchemy.exc.SQLAlchemyError("IGNORE THIS ERROR")

    def test_scoped_session2(self):
        with self.db.scoped_session(rollback=True, fail=False):
            raise sqlalchemy.exc.SQLAlchemyError("IGNORE THIS ERROR")
