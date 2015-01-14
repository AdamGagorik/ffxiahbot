import unittest
import logging
logging.getLogger().setLevel(logging.DEBUG)

from ...tables.base import Base

class TestCase(unittest.TestCase):
    def setUp(self):
        self.base = Base()

    def test_init(self):
        pass

if __name__ == '__main__':
    unittest.main()