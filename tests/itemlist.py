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

    def test_add1(self):
        ilist = pydarkstar.itemlist.ItemList()
        ilist.add(0)
        ilist.add(1)

    def test_add2(self):
        ilist = pydarkstar.itemlist.ItemList()

        ilist.add(0)
        with self.assertRaises(KeyError):
            ilist.add(0)

    def test_getitem(self):
        ilist = pydarkstar.itemlist.ItemList()
        i0 = ilist.add(0)
        self.assertEqual(id(i0), id(ilist[0]))

if __name__ == '__main__':
    unittest.main()
