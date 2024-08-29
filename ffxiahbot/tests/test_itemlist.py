import contextlib
import os
import tempfile
import unittest
from typing import Any, ClassVar

import_error = False
try:
    from ffxiahbot.item import Item
    from ffxiahbot.itemlist import ItemList
except ImportError:
    import_error = True
    ItemList = None
    Item = None


class TestCase00(unittest.TestCase):
    def test_import(self):
        self.assertFalse(import_error)


class TestCase01(unittest.TestCase):
    def setUp(self):
        if import_error:
            self.skipTest("ImportError")
        else:
            self.ilist = ItemList()

    def test_init(self):
        pass

    def test_add1(self):
        self.ilist.add(0)
        self.ilist.add(1)

    def test_add2(self):
        self.ilist.add(0)
        with self.assertRaises(KeyError):
            self.ilist.add(0)

    def test_set(self):
        self.ilist.add(0)
        self.ilist.add(1)
        self.ilist.set(0, 1, price_single=5)
        self.assertEqual(self.ilist[0].price_single, 5)
        self.assertEqual(self.ilist[1].price_single, 5)

    def test_getitem(self):
        i0 = self.ilist.add(0)
        self.assertEqual(id(i0), id(self.ilist[0]))

    def test_len(self):
        self.ilist.add(0)
        self.ilist.add(1)
        self.assertEqual(len(self.ilist), 2)

    _test_item1: ClassVar[list[Any]] = [0, "A", True, False, 10, 20, False, True, 30, 40]

    def test_savecsv(self):
        self.ilist.add(*self._test_item1)
        i, fname = tempfile.mkstemp()
        self.ilist.savecsv(fname)
        with open(fname) as handle:
            handle.readline().strip()
            handle.readline().strip()
        with contextlib.suppress(OSError):
            os.remove(fname)

    def test_loadcsv(self):
        ilist1 = ItemList()
        ilist1.add(*self._test_item1)
        i, fname = tempfile.mkstemp()
        ilist1.savecsv(fname)

        ilist2 = ItemList()
        ilist2.loadcsv(fname)

        for k in Item.keys:
            attr1 = getattr(ilist1.get(0), k)
            attr2 = getattr(ilist2.get(0), k)
            self.assertEqual(attr1, attr2)

    @staticmethod
    def _get_ilist(text, ilist):
        i, fname = tempfile.mkstemp()
        with open(fname, "w") as handle:
            handle.write(text)

        ilist.loadcsv(fname)
        with contextlib.suppress(OSError):
            os.remove(fname)

    def test_loadcsv2(self):
        text = """
itemid, name # comment 0
     0,    A
     2,    B
     4,    C # comment 1
itemid, name, price_single, rate_single
     6,    D,      10,    1.0
"""[1:-1]
        self._get_ilist(text, self.ilist)
        self.assertEqual(self.ilist[0].name, "A")
        self.assertEqual(self.ilist[2].name, "B")
        self.assertEqual(self.ilist[4].name, "C")
        self.assertEqual(self.ilist[6].name, "D")
        self.assertEqual(self.ilist[0].price_single, 1)
        self.assertEqual(self.ilist[2].price_single, 1)
        self.assertEqual(self.ilist[4].price_single, 1)
        self.assertEqual(self.ilist[6].price_single, 10)

    def test_loadcsv3(self):
        text = """
itemid, price_single
     0,    -1.0
"""[1:-1]
        with self.assertRaises(ValueError):
            self._get_ilist(text, self.ilist)

    def test_loadcsv4(self):
        text1 = """
itemid, name # comment 0
     0,    A
"""[1:-1]

        text2 = """
itemid, name # comment 0
     1,    B
"""[1:-1]

        ilist = ItemList()

        i, fname = tempfile.mkstemp()
        with open(fname, "w") as handle:
            handle.write(text1)

        ilist.loadcsv(fname)
        with contextlib.suppress(OSError):
            os.remove(fname)

        i, fname = tempfile.mkstemp()
        with open(fname, "w") as handle:
            handle.write(text2)

        ilist.loadcsv(fname)
        with contextlib.suppress(OSError):
            os.remove(fname)

        self.assertTrue(len(ilist), 2)
