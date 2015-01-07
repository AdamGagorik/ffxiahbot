import unittest
import pydarkstar.logutils
import pydarkstar.darkobject

pydarkstar.logutils.setDebug()

class TestCase(unittest.TestCase):
    def test_init(self):
        pydarkstar.darkobject.DarkObject()

if __name__ == '__main__':
    unittest.main()