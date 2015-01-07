import unittest
import pydarkstar.logutils
import pydarkstar.itemlist
import tempfile
import os
import re

pydarkstar.logutils.setDebug()

class TestCase(unittest.TestCase):
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

    _test_item1 = [0, 'A', True, False, 10, 20, False, True, 30, 40]

    def test_savecsv(self):
        ilist = pydarkstar.itemlist.ItemList()
        ilist.add(*self._test_item1)
        i, fname = tempfile.mkstemp()
        ilist.savecsv(fname)
        with open(fname, 'rb') as handle:
            line = handle.readline().strip()
            line = handle.readline().strip()
        os.remove(fname)

    def test_loadcsv(self):
        ilist1 = pydarkstar.itemlist.ItemList()
        ilist1.add(*self._test_item1)
        i, fname = tempfile.mkstemp()
        ilist1.savecsv(fname)

        ilist2 = pydarkstar.itemlist.ItemList()
        ilist2.loadcsv(fname)

        for k in pydarkstar.item.Item.keys:
            attr1 = getattr(ilist1.get(0), k)
            attr2 = getattr(ilist2.get(0), k)
            self.assertEqual(attr1, attr2)

    def _get_ilist(self, text):
        i, fname = tempfile.mkstemp()
        with open(fname, 'wb') as handle:
            handle.write(text)

        ilist = pydarkstar.itemlist.ItemList()
        ilist.loadcsv(fname)
        os.remove(fname)
        return ilist

    def test_loadcsv2(self):
        text = \
"""
itemid, name # comment 0
     0,    A
     2,    B
     4,    C # comment 1
itemid, name, price01
     6,    D,      10
"""[1:-1]
        ilist = self._get_ilist(text)
        self.assertEqual(ilist[0].name, 'A')
        self.assertEqual(ilist[2].name, 'B')
        self.assertEqual(ilist[4].name, 'C')
        self.assertEqual(ilist[6].name, 'D')
        self.assertEqual(ilist[0].price01,  1)
        self.assertEqual(ilist[2].price01,  1)
        self.assertEqual(ilist[4].price01,  1)
        self.assertEqual(ilist[6].price01, 10)

    def test_loadcsv3(self):
        text = \
"""
itemid, price01
     0,    -1.0
"""[1:-1]
        with self.assertRaises(ValueError):
            ilist = self._get_ilist(text)

if __name__ == '__main__':
    unittest.main()
