from pydarkstar.tables.auctionhouse import AuctionHouse
import pydarkstar.auction.worker
import pydarkstar.database
import pydarkstar.itemlist
import sqlalchemy

class Manager(pydarkstar.auction.worker.Worker):
    """
    Auction House browser.

    :param db: database object
    """
    def __init__(self, db, *args, **kwargs):
        super(Manager, self).__init__(db, *args, **kwargs)
        self.blacklist = set()

    def buyItems(self, itemdata):
        pass

    def restockItems(self, itemdata):
        pass

if __name__ == '__main__':
    pass