import unittest

from ffxiahbot.tables.deliverybox import DeliveryBox


class TestCase01(unittest.TestCase):
    def setUp(self):
        self.db = DeliveryBox()

    def test_init(self):
        pass

    def test_str(self):
        str(self.db)
