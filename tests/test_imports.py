import unittest
import logging

class TestCase0(unittest.TestCase):
    def test_pydarkstar(self):
        import pydarkstar
        logging.debug(pydarkstar.__name__)

    def test_pydarkstar_logutils(self):
        import pydarkstar.logutils
        pydarkstar.logutils.set_debug()
        logging.debug(pydarkstar.logutils.__name__)

class TestCase1(unittest.TestCase):
    def test_pydarkstar_common(self):
        import pydarkstar.common
        logging.debug(pydarkstar.common.__name__)

    def test_pydarkstar_darkobject(self):
        import pydarkstar.darkobject
        logging.debug(pydarkstar.darkobject.__name__)

    def test_pydarkstar_database(self):
        import pydarkstar.database
        logging.debug(pydarkstar.database.__name__)

    def test_pydarkstar_item(self):
        import pydarkstar.item
        logging.debug(pydarkstar.item.__name__)

    def test_pydarkstar_itemlist(self):
        import pydarkstar.itemlist
        logging.debug(pydarkstar.itemlist.__name__)

    def test_pydarkstar_options(self):
        import pydarkstar.options
        logging.debug(pydarkstar.options.__name__)

    def test_pydarkstar_timeutils(self):
        import pydarkstar.timeutils
        logging.debug(pydarkstar.timeutils.__name__)

class TestCase2(unittest.TestCase):
    def test_scrubbing(self):
        import pydarkstar.scrubbing
        logging.debug(pydarkstar.scrubbing.__name__)

    def test_scrubbing_scrubber(self):
        import pydarkstar.scrubbing.scrubber
        logging.debug(pydarkstar.scrubbing.scrubber.__name__)

    def test_scrubbing_ffxiah(self):
        import pydarkstar.scrubbing.ffxiah
        logging.debug(pydarkstar.scrubbing.ffxiah.__name__)

class TestCase3(unittest.TestCase):
    def test_tables(self):
        import pydarkstar.tables
        logging.debug(pydarkstar.tables.__name__)

    def test_tables_base(self):
        import pydarkstar.tables.base
        logging.debug(pydarkstar.tables.base.__name__)

    def test_tables_auctionhouse(self):
        import pydarkstar.tables.auctionhouse
        logging.debug(pydarkstar.tables.auctionhouse.__name__)

    def test_tables_deliverybox(self):
        import pydarkstar.tables.deliverybox
        logging.debug(pydarkstar.tables.deliverybox.__name__)

class TestCase4(unittest.TestCase):
    def test_auction(self):
        import pydarkstar.auction
        logging.debug(pydarkstar.auction.__name__)

    def test_auction_browser(self):
        import pydarkstar.auction.browser
        logging.debug(pydarkstar.auction.browser.__name__)

    def test_auction_buyer(self):
        import pydarkstar.auction.buyer
        logging.debug(pydarkstar.auction.buyer.__name__)

    def test_auction_cleaner(self):
        import pydarkstar.auction.cleaner
        logging.debug(pydarkstar.auction.cleaner.__name__)

    def test_auction_manager(self):
        import pydarkstar.auction.manager
        logging.debug(pydarkstar.auction.manager.__name__)

    def test_auction_seller(self):
        import pydarkstar.auction.seller
        logging.debug(pydarkstar.auction.seller.__name__)

    def test_auction_worker(self):
        import pydarkstar.auction.worker
        logging.debug(pydarkstar.auction.worker.__name__)

if __name__ == '__main__':
    unittest.main()