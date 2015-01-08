from pydarkstar.tables.auctionhouse import AuctionHouse
import pydarkstar.auction.worker
import pydarkstar.database
import pydarkstar.itemlist
import pydarkstar.auction.browser
import pydarkstar.auction.cleaner
import pydarkstar.auction.seller
import pydarkstar.auction.buyer
import sqlalchemy

class Manager(pydarkstar.auction.worker.Worker):
    """
    Auction House browser.

    :param db: database object
    """
    def __init__(self, db, **kwargs):
        super(Manager, self).__init__(db, **kwargs)
        self.blacklist = set()
        self.browser = pydarkstar.auction.browser.Browser(db, **kwargs)
        self.cleaner = pydarkstar.auction.cleaner.Cleaner(db, **kwargs)
        self.seller  = pydarkstar.auction.seller.Seller(db, **kwargs)
        self.buyer   = pydarkstar.auction.buyer.Buyer(db, **kwargs)

    def buyItems(self, itemdata):
        pass

    def restockItems(self, itemdata):
        pass

if __name__ == '__main__':
    pass