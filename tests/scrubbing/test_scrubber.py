import unittest

from ffxiahbot.scrubbing.scrubber import Scrubber


class TestCase01(unittest.TestCase):
    def test_init(self):
        Scrubber()
