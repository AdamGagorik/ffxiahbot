"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import unittest
import pydarkstar.logutils
import pydarkstar.scrub.ffxiah

pydarkstar.logutils.setDebug()

class TestFFXIAH(unittest.TestCase):
    def test_getCategoryURLs(self):
        pydarkstar.scrub.ffxiah.getCategoryURLs()

    def test_scrubCategoryURL(self):
        pydarkstar.scrub.ffxiah.scrubCategoryURL(r'http://www.ffxiah.com/browse/49/ninja-tools')

    def test_getItemids(self):
        urls=['http://www.ffxiah.com/browse/56/breads-rice']
        pydarkstar.scrub.ffxiah.getItemids(urls, force=False, save=None)

if __name__ == '__main__':
    unittest.main()