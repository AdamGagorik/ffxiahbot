import unittest
import logging

logging.getLogger().setLevel(logging.DEBUG)

from ..options import Options


class TestCase(unittest.TestCase):
    def setUp(self):
        self.opts = Options()

    def test_init(self):
        pass
