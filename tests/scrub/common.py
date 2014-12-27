"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import unittest
import pydarkstar.logutils
import pydarkstar.scrub.common

pydarkstar.logutils.setDebug()

class TestCommon(unittest.TestCase):
    def test_soup(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()