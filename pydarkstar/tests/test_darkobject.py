import unittest
import logging
logging.getLogger().setLevel(logging.DEBUG)

from ..darkobject import DarkObject

class TestCase(unittest.TestCase):
    def setUp(self):
        self.do = DarkObject()

    def test_init(self):
        pass