"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import unittest
import pydarkstar.logutils
import pydarkstar.item

pydarkstar.logutils.setDebug()

class TestItem(unittest.TestCase):
    def test_init(self):
        pydarkstar.item.Item()

if __name__ == '__main__':
    unittest.main()
