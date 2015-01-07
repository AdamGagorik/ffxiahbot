from pydarkstar.tables.auctionhouse import AuctionHouse
import pydarkstar.auction.worker
import pydarkstar.database
import pydarkstar.itemlist

class Buyer(pydarkstar.auction.worker.Worker):
    """
    Auction House buyer.

    :param db: database object
    """
    def __init__(self, db, buyer_name='Zissou', *args, **kwargs):
        super(Buyer, self).__init__(db, *args, **kwargs)
        self.buyer_name = str(buyer_name)

    def buyItem(self, row, date, price):
        """
        Buy item for given price.
        """
        # validate
        if row.sale == 0:
            self.error('item already sold!')
            return

        row.buyer_name = AuctionHouse.validate_seller(self.buyer_name)
        row.sell_date  = AuctionHouse.validate_date(date)
        row.sale       = AuctionHouse.validate_price(price)
        self.info('%s', row)

if __name__ == '__main__':
    pass