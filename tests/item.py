"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import unittest
import pydarkstar.logutils
import pydarkstar.item

pydarkstar.logutils.setDebug()

class TestItem(unittest.TestCase):
    def test_init(self):
        i0 = pydarkstar.item.Item(0, 'A')
        self.assertEqual(i0.itemid,  0 )
        self.assertEqual(i0.name  , 'A')

if __name__ == '__main__':
    unittest.main()
