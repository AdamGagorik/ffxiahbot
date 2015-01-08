from pydarkstar.tables.auctionhouse import AuctionHouse
import pydarkstar.auction.worker
import pydarkstar.database

class Cleaner(pydarkstar.auction.worker.Worker):
    """
    Auction House cleaner.

    :param db: database object
    """
    def __init__(self, db, **kwargs):
        super(Cleaner, self).__init__(db, **kwargs)

    def clear(self, seller=None):
        """
        Clear out auction house.
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