import unittest
import pydarkstar.logutils
import pydarkstar.scrub.scrubber

pydarkstar.logutils.setDebug()

class TestCase(unittest.TestCase):
    def test_init(self):
        pydarkstar.scrub.scrubber.Scrubber()

if __name__ == '__main__':
    unittest.main()