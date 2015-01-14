from ..tables.auctionhouse import AuctionHouse
from .. import timeutils
from . import worker
from . import browser
from . import cleaner
from . import seller
from . import buyer
import datetime

class Manager(worker.Worker):
    """
    Auction House browser.

    :param db: database object
    """
    def __init__(self, db, **kwargs):
        super(Manager, self).__init__(db, **kwargs)
        self.blacklist = set()
        self.browser = browser.Browser(db, **kwargs)
        self.cleaner = cleaner.Cleaner(db, **kwargs)
        self.seller  = seller.Seller(db, **kwargs)
        self.buyer   = buyer.Buyer(db, **kwargs)

    def addToBlacklist(self, rowid):
        """
        Add row to blacklist.
        """
        self.info('blacklisting: row=%d', rowid)
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
                                        date = timeutils.timestamp(datetime.datetime.now())
                                        self.buyer.buyItem(row, date, data.price12)
                                    else:
                                        self.info('price too high! itemid=%d %d <= %d',
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
                                        date = timeutils.timestamp(datetime.datetime.now())
                                        self.buyer.buyItem(row, date, data.price01)
                                    else:
                                        self.info('price too high! itemid=%d %d <= %d',
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
        """
        The main restock loop.
        """
        # loop over items
        for data in itemdata.items.values():

            # singles
            if data.sell01:
                # check history
                history_price = self.browser.getPrice(itemid=data.itemid, stack=False, seller=self.seller.seller)

                # set history
                if history_price is None or history_price <= 0:
                    now = timeutils.timestamp(datetime.datetime.now())
                    self.seller.setHistory(itemid=data.itemid, stack=False, price=data.price01, date=now, count=1)

                # get stock
                stock = self.browser.getStock(itemid=data.itemid, stack=False, seller=self.seller.seller)

                # restock
                while stock < data.stock01:
                    now = timeutils.timestamp(datetime.datetime.now())
                    self.seller.sellItem(itemid=data.itemid, stack=False, date=now, price=data.price01, count=1)
                    stock += 1

            # stacks
            if data.sell12:
                # check history
                history_price = self.browser.getPrice(itemid=data.itemid, stack=True, seller=self.seller.seller)

                # set history
                if history_price is None or history_price <= 0:
                    now = timeutils.timestamp(datetime.datetime.now())
                    self.seller.setHistory(itemid=data.itemid, stack=True, price=data.price12, date=now, count=1)

                # get stock
                stock = self.browser.getStock(itemid=data.itemid, stack=True, seller=self.seller.seller)

                # restock
                while stock < data.stock01:
                    now = timeutils.timestamp(datetime.datetime.now())
                    self.seller.sellItem(itemid=data.itemid, stack=True, date=now, price=data.price12, count=1)
                    stock += 1

if __name__ == '__main__':
    pass
