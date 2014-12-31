"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import unittest
import pydarkstar.logutils
import pydarkstar.common
import os

pydarkstar.logutils.setDebug()

class TestCommon(unittest.TestCase):
    def test_backup1(self):
        path = pydarkstar.common.backup('common.pz', copy=False)
        self.assertEqual(path, '')

    def test_backup2(self):
        path = pydarkstar.common.backup('common.py', copy=False)
        self.assertEqual(os.path.dirname(path), os.getcwd())
        self.assertEqual(os.path.basename(path), 'common.py.1')

if __name__ == '__main__':
    unittest.main()