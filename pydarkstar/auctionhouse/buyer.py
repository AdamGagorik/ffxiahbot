"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
from pydarkstar.tables.auctionhouse import AuctionHouse
import pydarkstar.auctionhouse.auctionbase
import pydarkstar.auctionhouse.browser
import pydarkstar.database

class Buyer(pydarkstar.auctionhouse.auctionbase.AuctionBase):
    """
    Auction House buyer.

    :param db: database object
    """
    def __init__(self, db, buyer_name='Zissou', *args, **kwargs):
        super(Buyer, self).__init__(db, *args, **kwargs)
        self.buyer_name = str(buyer_name)
        self.browser = pydarkstar.auctionhouse.browser.Browser(db)
        self.blacklist = set()

    def buyItem(self, row, date, price):
        """
        Buy item for given price.
        """
        history_price = self.browser.getPrice(row.itemid, row.stack)

        # only buy items for a price less than or equal to the history
        if price <= history_price:
            row.buyer_name = AuctionHouse.validate_seller(self.buyer_name)
            row.sell_date  = AuctionHouse.validate_date(date)
            row.sale       = AuctionHouse.validate_price(price)

        else:
            self.error('item price too high: %d > %d, seller=%s', price, history_price, row.seller)
            self.blacklist.add(row.id)

if __name__ == '__main__':
    pass