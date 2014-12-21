"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import unittest
import pydarkstar.logutils
import pydarkstar.itemlist

pydarkstar.logutils.setDebug()

class TestItemList(unittest.TestCase):
    def test_init(self):
        pydarkstar.itemlist.ItemList()

if __name__ == '__main__':
    unittest.main()
