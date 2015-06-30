import unittest

import_error = False
try:
    from ..item import Item
except ImportError:
    import_error = True
    Item = None


class TestCase00(unittest.TestCase):
    def test_import(self):
        self.assertFalse(import_error)


class TestCase01(unittest.TestCase):
    def setUp(self):
        if import_error:
            self.skipTest('ImportError')

    def test_init(self):
        i0 = Item(0, 'A')
        self.assertEqual(i0.itemid, 0)
        self.assertEqual(i0.name, 'A')

    def test_price01(self):
        Item(0, price01=+1)
        with self.assertRaises(ValueError):
            Item(0, price01=+0)

        with self.assertRaises(ValueError):
            Item(0, price01=-1)

    def test_price12(self):
        Item(0, price12=+1)
        with self.assertRaises(ValueError):
            Item(0, price12=+0)

        with self.assertRaises(ValueError):
            Item(0, price12=-1)

    def test_stock01(self):
        Item(0, stock01=+0)

        with self.assertRaises(ValueError):
            Item(0, stock01=-1)

    def test_stock12(self):
        Item(0, stock12=+0)

        with self.assertRaises(ValueError):
            Item(0, stock12=-1)

    def test_rate01(self):
        i = Item(0)
        self.assertEqual(i.rate01, 1.0)

        Item(0, rate01=0.0)
        Item(0, rate01=0.5)
        Item(0, rate01=1.0)

        with self.assertRaises(ValueError):
            Item(0, rate01=-1.5)

        with self.assertRaises(ValueError):
            Item(0, rate01=+1.5)

    def test_rate12(self):
        i = Item(0)
        self.assertEqual(i.rate12, 1.0)

        Item(0, rate12=0.0)
        Item(0, rate12=0.5)
        Item(0, rate12=1.0)

        with self.assertRaises(ValueError):
            Item(0, rate12=-1.5)

        with self.assertRaises(ValueError):
            Item(0, rate12=+1.5)
