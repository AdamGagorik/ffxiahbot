"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import unittest
import pydarkstar.logutils
import pydarkstar.scrub.ffxiah

pydarkstar.logutils.setInfo()

class TestFFXIAHScrubber(unittest.TestCase):
    def test_get_category_urls(self):
        scrubber = pydarkstar.scrub.ffxiah.FFXIAHScrubber()
        scrubber._get_category_urls()

    def test_get_itemids_for_category_url(self):
        url = r'http://www.ffxiah.com/browse/49/ninja-tools'
        scrubber = pydarkstar.scrub.ffxiah.FFXIAHScrubber()
        scrubber._get_itemids_for_category_url(url)

    def test_get_itemids(self):
        urls=[
            r'http://www.ffxiah.com/browse/49/ninja-tools',
            r'http://www.ffxiah.com/browse/56/breads-rice',
        ]
        scrubber = pydarkstar.scrub.ffxiah.FFXIAHScrubber()
        scrubber._get_itemids(urls)

    def test_get_item_data_for_itemid(self):
        scrubber = pydarkstar.scrub.ffxiah.FFXIAHScrubber()
        scrubber._get_item_data_for_itemid(4096)

    def test_get_item_data(self):
        scrubber = pydarkstar.scrub.ffxiah.FFXIAHScrubber()
        scrubber._get_item_data(list(range(1, 9)), threads=4)

    def test_scrub(self):
        scrubber = pydarkstar.scrub.ffxiah.FFXIAHScrubber()
        scrubber.scrub(force=True, threads=4, ids=[1, 2, 3, 4])

if __name__ == '__main__':
    unittest.main()