import unittest
import pydarkstar.logutils
import pydarkstar.scrubbing.scrubber

pydarkstar.logutils.setDebug()

class TestCase(unittest.TestCase):
    def test_init(self):
        pydarkstar.scrubbing.scrubber.Scrubber()

if __name__ == '__main__':
    unittest.main()