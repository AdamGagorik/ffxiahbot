import unittest
import logging

logging.getLogger().setLevel(logging.DEBUG)

from ...scrubbing.scrubber import Scrubber


class TestCase(unittest.TestCase):
    def setUp(self):
        self.scrubber = Scrubber()

    def test_init(self):
        pass
