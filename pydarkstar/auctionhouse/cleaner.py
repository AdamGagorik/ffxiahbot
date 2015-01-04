"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
from pydarkstar.tables.auctionhouse import AuctionHouse
import pydarkstar.auctionhouse.auctionbase
import pydarkstar.database

class Cleaner(pydarkstar.auctionhouse.auctionbase.AuctionBase):
    """
    Auction House cleaner.

    :param db: database object
    """
    def __init__(self, db, *args, **kwargs):
        super(Cleaner, self).__init__(db, *args, **kwargs)

    def clear(self, seller=None):
        """
        Clear out auctionhouse house.
        """
        # clear rows
        if seller is None:

            # perform query
            with self.scopped_session() as session:
                N = session.query(AuctionHouse).delete()
                self.info('%d rows dropped', N)

        # clear rows of seller
        else:

            # validate seller
            with self.capture(fail=self.fail):
                if not isinstance(seller, int) or not seller >= 0:
                    raise RuntimeError('invalid seller: %s', seller)

                # perform query
                with self.scopped_session() as session:
                    N = session.query(AuctionHouse).filter(
                        AuctionHouse.seller == seller,
                    ).delete()
                    self.info('%d rows dropped', N)

if __name__ == '__main__':
    pass