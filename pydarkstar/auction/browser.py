from pydarkstar.tables.auctionhouse import AuctionHouse
import pydarkstar.auction.worker
import pydarkstar.database
import sqlalchemy

class Browser(pydarkstar.auction.worker.Worker):
    """
    Auction House browser.

    :param db: database object
    """
    def __init__(self, db, *args, **kwargs):
        super(Browser, self).__init__(db, *args, **kwargs)

    def count(self):
        """
        Get the number of rows.
        """
        with self.scopped_session() as session:
            return session.query(AuctionHouse).count()

    def getStock(self, itemid, stack=False, seller=None):
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
            stack  = AuctionHouse.validate_stack(stack)

            # perform query
            with self.scopped_session() as session:

                # ignore seller
                if seller is None:
                    N = session.query(AuctionHouse).filter(
                        AuctionHouse.itemid == itemid,
                        AuctionHouse.stack  == stack,
                        AuctionHouse.sale   == 0,
                    ).count()
                    return N

                # consider seller
                else:
                    seller = AuctionHouse.validate_seller(seller)
                    N = session.query(AuctionHouse).filter(
                        AuctionHouse.itemid == itemid,
                        AuctionHouse.seller == seller,
                        AuctionHouse.stack  == stack,
                        AuctionHouse.sale   == 0,
                    ).count()
                    return N

    def getPrice(self, itemid, stack=False, seller=None, func=sqlalchemy.func.min):
        """
        Get price of item.

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
            stack  = AuctionHouse.validate_stack(stack)

            # perform query
            with self.scopped_session() as session:

                # ignore seller
                if seller is None:
                    N = session.query(func(AuctionHouse.sale)).filter(
                        AuctionHouse.itemid == itemid,
                        AuctionHouse.stack  == stack,
                        AuctionHouse.sale   != 0,
                    ).scalar()
                    return N

                # consider seller
                else:
                    seller = AuctionHouse.validate_seller(seller)
                    N = session.query(func(AuctionHouse.sale)).filter(
                        AuctionHouse.itemid == itemid,
                        AuctionHouse.seller == seller,
                        AuctionHouse.stack  == stack,
                        AuctionHouse.sale   != 0,
                    ).scalar()
                    return N

if __name__ == '__main__':
    pass