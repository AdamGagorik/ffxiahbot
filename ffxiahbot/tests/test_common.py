import os
import unittest

import_error = False
try:
    from ffxiahbot import common
except ImportError:
    import_error = True
    common = None


class TestCase00(unittest.TestCase):
    def test_import(self):
        self.assertFalse(import_error)


class TestCase01(unittest.TestCase):
    def setUp(self):
        if import_error:
            self.skipTest("ImportError")

    def test_backup1(self):
        path = common.backup("common.pz", copy=False)
        self.assertEqual(path, "")

    def test_backup2(self):
        path = common.backup(os.path.join(os.path.dirname(__file__), "test_common.py"), copy=False)
        self.assertEqual(os.path.dirname(path), os.path.dirname(__file__))
        self.assertEqual(os.path.basename(path), "test_common.py.1")
