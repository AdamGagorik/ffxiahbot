"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import unittest
import pydarkstar.logutils
import pydarkstar.itemlist
import tempfile
import os

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

    def test_set(self):
        ilist = pydarkstar.itemlist.ItemList()
        ilist.add(0)
        ilist.add(1)
        ilist.set(0, 1, price01=5)
        self.assertEqual(ilist[0].price01, 5)
        self.assertEqual(ilist[1].price01, 5)

    def test_getitem(self):
        ilist = pydarkstar.itemlist.ItemList()
        i0 = ilist.add(0)
        self.assertEqual(id(i0), id(ilist[0]))

    def test_len(self):
        ilist = pydarkstar.itemlist.ItemList()
        ilist.add(0)
        ilist.add(1)
        self.assertEqual(len(ilist), 2)

    def test_savecsv(self):
        ilist = pydarkstar.itemlist.ItemList()
        ilist.add(0, 'A', True, True, 10, 20, False, False, 30, 40)
        i, fname = tempfile.mkstemp()
        ilist.savecsv(fname)
        with open(fname, 'rb') as handle:
            line = handle.readline().strip()
            line = handle.readline().strip()
            self.assertEqual(line, '0,A,True,True,10,20,False,False,30,40')
        os.remove(fname)

if __name__ == '__main__':
    unittest.main()
