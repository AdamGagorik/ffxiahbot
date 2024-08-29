import unittest

from ffxiahbot.tables.base import Base


class TestCase01(unittest.TestCase):
    def setUp(self):
        self.base = Base()

    def test_init(self):
        pass
