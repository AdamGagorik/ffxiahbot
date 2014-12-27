"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import unittest
import pydarkstar.logutils
import pydarkstar.scrub.scrubber

pydarkstar.logutils.setDebug()

class TestScrubber(unittest.TestCase):
    def test_init(self):
        pydarkstar.scrub.scrubber.Scrubber()

if __name__ == '__main__':
    unittest.main()