import unittest

from ffxiahbot.item import Item


class TestCase01(unittest.TestCase):
    def test_init(self):
        i0 = Item(itemid=0, name="A")
        self.assertEqual(i0.itemid, 0)
        self.assertEqual(i0.name, "A")

    def test_price_single(self):
        Item(itemid=0, price_single=+1)
        with self.assertRaises(ValueError):
            Item(itemid=0, price_single=+0)

        with self.assertRaises(ValueError):
            Item(itemid=0, price_single=-1)

    def test_price_stacks(self):
        Item(itemid=0, price_stacks=+1)
        with self.assertRaises(ValueError):
            Item(itemid=0, price_stacks=+0)

        with self.assertRaises(ValueError):
            Item(itemid=0, price_stacks=-1)

    def test_stock_single(self):
        Item(itemid=0, stock_single=+0)

        with self.assertRaises(ValueError):
            Item(itemid=0, stock_single=-1)

    def test_stock_stacks(self):
        Item(itemid=0, stock_stacks=+0)

        with self.assertRaises(ValueError):
            Item(itemid=0, stock_stacks=-1)

    def test_rate_single(self):
        i = Item(itemid=0)
        self.assertEqual(i.rate_single, 1.0)

        Item(itemid=0, rate_single=0.0)
        Item(itemid=0, rate_single=0.5)
        Item(itemid=0, rate_single=1.0)

        with self.assertRaises(ValueError):
            Item(itemid=0, rate_single=-1.5)

        with self.assertRaises(ValueError):
            Item(itemid=0, rate_single=+1.5)

    def test_rate_stacks(self):
        i = Item(itemid=0)
        self.assertEqual(i.rate_stacks, 1.0)

        Item(itemid=0, rate_stacks=0.0)
        Item(itemid=0, rate_stacks=0.5)
        Item(itemid=0, rate_stacks=1.0)

        with self.assertRaises(ValueError):
            Item(itemid=0, rate_stacks=-1.5)

        with self.assertRaises(ValueError):
            Item(itemid=0, rate_stacks=+1.5)
