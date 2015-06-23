import unittest

import_error = False
try:
    from ..options import Options
except ImportError:
    import_error = True
    Options = None


class TestCase00(unittest.TestCase):
    def test_import(self):
        self.assertFalse(import_error)


class TestCase01(unittest.TestCase):
    def setUp(self):
        if import_error:
            self.skipTest('ImportError')
        else:
            self.opts = Options()
