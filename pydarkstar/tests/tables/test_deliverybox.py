import unittest
import logging
logging.getLogger().setLevel(logging.DEBUG)

from ...tables.deliverybox import DeliveryBox

class TestCase(unittest.TestCase):
    def setUp(self):
        self.db = DeliveryBox()

    def test_init(self):
        pass

    def test_str(self):
        logging.debug(self.db)