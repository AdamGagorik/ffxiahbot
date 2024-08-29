import unittest

import_error = False
try:
    from ffxiahbot import logutils
except ImportError:
    import_error = True
    logutils = None


class TestCase00(unittest.TestCase):
    def test_import(self):
        self.assertFalse(import_error)
