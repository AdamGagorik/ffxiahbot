import unittest

import_error = False
try:
    from ffxiahbot.tables.base import Base
except ImportError:
    import_error = True
    Base = None


class TestCase00(unittest.TestCase):
    def test_import(self):
        self.assertFalse(import_error)


class TestCase01(unittest.TestCase):
    def setUp(self):
        self.base = Base()

    def test_init(self):
        pass
