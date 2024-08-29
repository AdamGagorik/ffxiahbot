import unittest

import_error = False
try:
    from ffxiahbot.tables.deliverybox import DeliveryBox
except ImportError:
    import_error = True
    DeliveryBox = None


class TestCase00(unittest.TestCase):
    def test_import(self):
        self.assertFalse(import_error)


class TestCase01(unittest.TestCase):
    def setUp(self):
        self.db = DeliveryBox()

    def test_init(self):
        pass

    def test_str(self):
        str(self.db)
