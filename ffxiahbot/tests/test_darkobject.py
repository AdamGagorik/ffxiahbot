import unittest

import_error = False
try:
    from ffxiahbot.darkobject import DarkObject
except ImportError:
    import_error = True
    DarkObject = None


class TestCase00(unittest.TestCase):
    def test_import(self):
        self.assertFalse(import_error)


class TestCase01(unittest.TestCase):
    def setUp(self):
        if import_error:
            self.skipTest("ImportError")
        else:
            self.do = DarkObject()

    def test_init(self):
        pass
