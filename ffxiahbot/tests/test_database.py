import unittest

import sqlalchemy.exc

from ffxiahbot.tests import sqltest

import_error = False
try:
    from ffxiahbot.database import Database
except ImportError:
    import_error = True
    Database = None


class TestCase00(unittest.TestCase):
    def test_import(self):
        self.assertFalse(import_error)


class TestCase01(sqltest.TestSQL):
    def setUp(self):
        if import_error:
            self.skipTest("ImportError")
        else:
            super().setUp()

    def test_scoped_session1(self):
        with self.assertRaises(RuntimeError), self.db.scoped_session(rollback=True, fail=True):
            raise sqlalchemy.exc.SQLAlchemyError("IGNORE THIS ERROR")

    def test_scoped_session2(self):
        with self.db.scoped_session(rollback=True, fail=False):
            raise sqlalchemy.exc.SQLAlchemyError("IGNORE THIS ERROR")
