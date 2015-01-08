from pydarkstar.tables.auctionhouse import AuctionHouse
import pydarkstar.auction.worker
import pydarkstar.database
import pydarkstar.itemlist
import pydarkstar.auction.browser
import pydarkstar.auction.cleaner
import pydarkstar.auction.seller
import pydarkstar.auction.buyer
import pydarkstar.timeutils
import datetime

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

    def addToBlacklist(self, rowid):
        """
        Add row to blacklist.
        """
        self.debug('blacklisting: row=%d', rowid)
        self.blacklist.add(rowid)

    def buyItems(self, itemdata):
        """
        The main buy item loop.
        """
        with self.scopped_session(fail=self.fail) as session:
            # find rows that are still up for sale
            q = session.query(AuctionHouse).filter(
                    AuctionHouse.seller    != self.seller.seller,
                    AuctionHouse.sell_date == 0,
                    AuctionHouse.sale      == 0,
                )
            # loop rows
            for row in q:
                with self.capture(fail=self.fail):
                    # skip blacklisted rows
                    if not row.id in self.blacklist:
                        # get item data
                        try:
                            data = itemdata[row.itemid]
                        except KeyError:
                            self.error('item missing from database: %d', row.itemid)
                            data = None

                        if not data is None:
                            # buy stacks
                            if row.stack:
                                # check permissions
                                if data.buy12:
                                    # check price
                                    if row.price <= data.price12:
                                        date = pydarkstar.timeutils.timestamp(datetime.datetime.now())
                                        self.buyer.buyItem(row, date, data.price12)
                                    else:
                                        self.debug('price too high! itemid=%d %d <= %d',
                                            row.itemid, row.price, data.price12)
                                        self.addToBlacklist(row.id)
                                else:
                                    self.debug('not allowed to buy item! itemid=%d', row.itemid)
                                    self.addToBlacklist(row.id)
                            # buy singles
                            else:
                                # check permissions
                                if data.buy01:
                                    # check price
                                    if row.price <= data.price01:
                                        date = pydarkstar.timeutils.timestamp(datetime.datetime.now())
                                        self.buyer.buyItem(row, date, data.price01)
                                    else:
                                        self.debug('price too high! itemid=%d %d <= %d',
                                            row.itemid, row.price, data.price01)
                                        self.addToBlacklist(row.id)
                                else:
                                    self.debug('not allowed to buy item! itemid=%d', row.itemid)
                                    self.addToBlacklist(row.id)
                        else:
                            # item data missing
                            self.addToBlacklist(row.id)
                    else:
                        # row was blacklisted
                        self.debug('skipping row %d', row.id)

    def restockItems(self, itemdata):
        pass

if __name__ == '__main__':
    pass