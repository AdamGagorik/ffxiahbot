from ffxiahbot.auction.worker import Worker
from ffxiahbot.tables.auctionhouse import AuctionHouse


class Cleaner(Worker):
    """
    Auction House cleaner.

    :param db: database object
    """

    def __init__(self, db, **kwargs):
        super().__init__(db, **kwargs)

    def clear(self, seller=None):
        """
        Clear out auction house.
        """
        # clear rows
        if seller is None:
            # perform query
            with self.scopped_session() as session:
                n = session.query(AuctionHouse).delete()
                self.info("%d rows dropped", n)

        # clear rows of seller
        else:
            # validate seller
            with self.capture(fail=self.fail):
                if not isinstance(seller, int) or not seller >= 0:
                    raise RuntimeError("invalid seller: %s", seller)

                # perform query
                with self.scopped_session() as session:
                    n = (
                        session.query(AuctionHouse)
                        .filter(
                            AuctionHouse.seller == seller,
                        )
                        .delete()
                    )
                    self.info("%d rows dropped", n)


if __name__ == "__main__":
    pass
