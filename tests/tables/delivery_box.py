"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import unittest
import pydarkstar.logutils
import pydarkstar.tables.delivery_box

pydarkstar.logutils.setDebug()

class TestDeliveryBox(unittest.TestCase):
    def test_init(self):
        pydarkstar.tables.delivery_box.DeliveryBox()

if __name__ == '__main__':
    unittest.main()