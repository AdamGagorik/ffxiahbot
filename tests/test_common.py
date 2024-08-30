import os
import unittest

from ffxiahbot import common


class TestCase01(unittest.TestCase):
    def test_backup1(self):
        path = common.backup("common.pz", copy=False)
        self.assertIsNone(path)

    def test_backup2(self):
        path = common.backup(os.path.join(os.path.dirname(__file__), "test_common.py"), copy=False)
        self.assertEqual(os.path.dirname(path), os.path.dirname(__file__))
        self.assertEqual(os.path.basename(path), "test_common.py.1")
