import unittest

import_error = False
try:
    from ffxiahbot.scrubbing.scrubber import Scrubber
except ImportError:
    import_error = True
    Scrubber = None


class TestCase00(unittest.TestCase):
    def test_import(self):
        self.assertFalse(import_error)


class TestCase01(unittest.TestCase):
    def setUp(self):
        if import_error:
            self.skipTest("ImportError")
        else:
            self.scrubber = Scrubber()

    def test_init(self):
        pass
