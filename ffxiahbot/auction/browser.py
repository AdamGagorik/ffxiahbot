import sqlalchemy

from ffxiahbot.auction.worker import Worker
from ffxiahbot.tables.auctionhouse import AuctionHouse


class Browser(Worker):
    """
    Auction House browser.

    :param db: database object
    """

    def __init__(self, db, **kwargs):
        super().__init__(db, **kwargs)

    def count(self):
        """
        Get the number of rows.
        """
        with self.scopped_session() as session:
            return session.query(AuctionHouse).count()

    def get_stock(self, itemid, stack=False, seller=None):
        """
        Get stock of item.

        :param itemid: item number
        :param stack: consider stacks
        :param seller: consider seller

        :type itemid: int
        :type stack: int
        :type seller: int
        """
        with self.capture(fail=self.fail):
            # validate
            itemid = AuctionHouse.validate_itemid(itemid)
            stack = AuctionHouse.validate_stack(stack)

            # perform query
            with self.scopped_session() as session:
                # ignore seller
                if seller is None:
                    n = (
                        session.query(AuctionHouse)
                        .filter(
                            AuctionHouse.itemid == itemid,
                            AuctionHouse.stack == stack,
                            AuctionHouse.sale == 0,
                        )
                        .count()
                    )
                    return n

                # consider seller
                else:
                    seller = AuctionHouse.validate_seller(seller)
                    n = (
                        session.query(AuctionHouse)
                        .filter(
                            AuctionHouse.itemid == itemid,
                            AuctionHouse.seller == seller,
                            AuctionHouse.stack == stack,
                            AuctionHouse.sale == 0,
                        )
                        .count()
                    )
                    return n

    def get_price(self, itemid, stack=False, seller=None, func=sqlalchemy.func.min):
        """
        Get price of item.

        :param itemid: item number
        :param stack: consider stacks
        :param seller: consider seller
        :param func: sqlalchemy function

        :type itemid: int
        :type stack: int
        :type seller: int
        """
        with self.capture(fail=self.fail):
            # validate
            itemid = AuctionHouse.validate_itemid(itemid)
            stack = AuctionHouse.validate_stack(stack)

            # perform query
            with self.scopped_session() as session:
                # ignore seller
                if seller is None:
                    n = (
                        session.query(func(AuctionHouse.sale))
                        .filter(
                            AuctionHouse.itemid == itemid,
                            AuctionHouse.stack == stack,
                            AuctionHouse.sale != 0,
                        )
                        .scalar()
                    )
                    return n

                # consider seller
                else:
                    seller = AuctionHouse.validate_seller(seller)
                    n = (
                        session.query(func(AuctionHouse.sale))
                        .filter(
                            AuctionHouse.itemid == itemid,
                            AuctionHouse.seller == seller,
                            AuctionHouse.stack == stack,
                            AuctionHouse.sale != 0,
                        )
                        .scalar()
                    )
                    return n


if __name__ == "__main__":
    pass
