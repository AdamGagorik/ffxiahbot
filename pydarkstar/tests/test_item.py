import unittest
import logging
logging.getLogger().setLevel(logging.DEBUG)

from ..item import Item

class TestCase(unittest.TestCase):
    def test_init(self):
        i0 = Item(0, 'A')
        self.assertEqual(i0.itemid,  0 )
        self.assertEqual(i0.name  , 'A')

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

if __name__ == '__main__':
    unittest.main()
