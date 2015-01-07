import unittest
import pydarkstar.logutils
import pydarkstar.item

pydarkstar.logutils.setDebug()

class TestCase(unittest.TestCase):
    def test_init(self):
        i0 = pydarkstar.item.Item(0, 'A')
        self.assertEqual(i0.itemid,  0 )
        self.assertEqual(i0.name  , 'A')

    def test_price01(self):
        pydarkstar.item.Item(0, price01=+1)
        with self.assertRaises(ValueError):
            pydarkstar.item.Item(0, price01=+0)

        with self.assertRaises(ValueError):
            pydarkstar.item.Item(0, price01=-1)

    def test_price12(self):
        pydarkstar.item.Item(0, price12=+1)
        with self.assertRaises(ValueError):
            pydarkstar.item.Item(0, price12=+0)

        with self.assertRaises(ValueError):
            pydarkstar.item.Item(0, price12=-1)

    def test_stock01(self):
        pydarkstar.item.Item(0, stock01=+0)

        with self.assertRaises(ValueError):
            pydarkstar.item.Item(0, stock01=-1)

    def test_stock12(self):
        pydarkstar.item.Item(0, stock12=+0)

        with self.assertRaises(ValueError):
            pydarkstar.item.Item(0, stock12=-1)

if __name__ == '__main__':
    unittest.main()
