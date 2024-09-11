import contextlib
import os
import tempfile
import unittest
from pathlib import Path
from typing import Any, ClassVar

from ffxiahbot.item import Item
from ffxiahbot.itemlist import ItemList


class TestCase01(unittest.TestCase):
    def setUp(self):
        self.item_list = ItemList()

    def test_init(self):
        pass

    def test_add1(self):
        self.item_list.add(0)
        self.item_list.add(1)

    def test_add2(self):
        self.item_list.add(0)
        with self.assertRaises(KeyError):
            self.item_list.add(0)

    def test_set(self):
        self.item_list.add(0)
        self.item_list.add(1)
        self.item_list.set(0, 1, price_single=5)
        self.assertEqual(self.item_list[0].price_single, 5)
        self.assertEqual(self.item_list[1].price_single, 5)

    def test_getitem(self):
        i0 = self.item_list.add(0)
        self.assertEqual(id(i0), id(self.item_list[0]))

    def test_len(self):
        self.item_list.add(0)
        self.item_list.add(1)
        self.assertEqual(len(self.item_list), 2)

    _test_item1: ClassVar[dict[str, Any]] = {
        "itemid": 0,
        "name": "A",
        "sell_single": True,
        "sell_stacks": False,
        "buy_single": False,
        "buy_stacks": True,
        "price_single": 10,
        "price_stacks": 20,
        "stock_single": 30,
        "stock_stacks": 40,
        "rate_single": 0.5,
        "rate_stacks": 0.6,
    }

    def test_save_csv(self):
        self.item_list.add(**self._test_item1)
        i, csv_path = tempfile.mkstemp()
        self.item_list.save_csv(Path(csv_path))
        with open(csv_path) as handle:
            handle.readline().strip()
            handle.readline().strip()
        with contextlib.suppress(OSError):
            os.remove(csv_path)

    def test_load_csv(self):
        item_list_1 = ItemList()
        item_list_1.add(**self._test_item1)
        i, csv_path = tempfile.mkstemp()
        item_list_1.save_csv(Path(csv_path))

        item_list_2 = ItemList()
        item_list_2.load_csv(Path(csv_path))

        for k in Item.model_fields:
            attr1 = getattr(item_list_1.get(0), k)
            attr2 = getattr(item_list_2.get(0), k)
            self.assertEqual(attr1, attr2)

    @staticmethod
    def _get_item_list(text, item_list):
        i, csv_path = tempfile.mkstemp()
        with open(csv_path, "w") as handle:
            handle.write(text)

        item_list.load_csv(csv_path)
        with contextlib.suppress(OSError):
            os.remove(csv_path)

    def test_load_csv2(self):
        text = """
itemid, name # comment 0
     0,    A
     2,    B
     4,    C # comment 1
itemid, name, price_single, rate_single
     6,    D,      10,    1.0
"""[1:-1]
        self._get_item_list(text, self.item_list)
        self.assertEqual(self.item_list[0].name, "A")
        self.assertEqual(self.item_list[2].name, "B")
        self.assertEqual(self.item_list[4].name, "C")
        self.assertEqual(self.item_list[6].name, "D")
        self.assertEqual(self.item_list[0].price_single, 1)
        self.assertEqual(self.item_list[2].price_single, 1)
        self.assertEqual(self.item_list[4].price_single, 1)
        self.assertEqual(self.item_list[6].price_single, 10)

    def test_load_csv3(self):
        text = """
itemid, price_single
     0,    -1.0
"""[1:-1]
        with self.assertRaises(ValueError):
            self._get_item_list(text, self.item_list)

    def test_load_csv4(self):
        text1 = """
itemid, name # comment 0
     0,    A
"""[1:-1]

        text2 = """
itemid, name # comment 0
     1,    B
"""[1:-1]

        item_list = ItemList()

        i, csv_path = tempfile.mkstemp()
        with open(csv_path, "w") as handle:
            handle.write(text1)

        item_list.load_csv(csv_path)
        with contextlib.suppress(OSError):
            os.remove(csv_path)

        i, csv_path = tempfile.mkstemp()
        with open(csv_path, "w") as handle:
            handle.write(text2)

        item_list.load_csv(csv_path)
        with contextlib.suppress(OSError):
            os.remove(csv_path)

        self.assertTrue(len(item_list), 2)
