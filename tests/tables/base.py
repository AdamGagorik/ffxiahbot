import unittest
import pydarkstar.logutils
import pydarkstar.tables.base

pydarkstar.logutils.setDebug()

class TestBase(unittest.TestCase):
    def test_init(self):
        pydarkstar.tables.base.Base()

if __name__ == '__main__':
    unittest.main()