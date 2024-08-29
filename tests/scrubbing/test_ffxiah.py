import unittest

from ffxiahbot.scrubbing.ffxiah import FFXIAHScrubber, extract


class TestCase01(unittest.TestCase):
    def setUp(self):
        self.scrubber = FFXIAHScrubber()
        self.scrubber.save = False

    def test_get_category_urls(self):
        self.scrubber._get_category_urls()

    def test_get_itemids_for_category_url(self):
        url = r"http://www.ffxiah.com/browse/49/ninja-tools"
        self.scrubber._get_itemids_for_category_url(url)

    def test_get_itemids(self):
        urls = [
            r"http://www.ffxiah.com/browse/49/ninja-tools",
            r"http://www.ffxiah.com/browse/56/breads-rice",
        ]
        self.scrubber._get_itemids(urls)

    def test_get_item_data_for_itemid(self):
        self.scrubber._get_item_data_for_itemid(4096)

    def test_get_item_data(self):
        self.scrubber._get_item_data(list(range(1, 9)))

    def test_scrub(self):
        self.scrubber.scrub(item_ids={1, 2, 3, 4})

    def test_extract(self):
        extract(self.scrubber._get_item_data([4096])[1], 4096)
