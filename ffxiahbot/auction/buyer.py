from ffxiahbot.auction.worker import Worker
from ffxiahbot.tables.auctionhouse import AuctionHouse


class Buyer(Worker):
    """
    Auction House buyer.

    :param db: database object
    """

    def __init__(self, db, buyer_name="Zissou", **kwargs):
        super().__init__(db, **kwargs)
        self.buyer_name = str(buyer_name)

    def buy_item(self, row, date, price):
        """
        Buy item for given price.
        """
        # validate
        if not row.sale == 0:
            raise RuntimeError("item already sold!")

        row.buyer_name = self.buyer_name
        row.sell_date = AuctionHouse.validate_date(date)
        row.sale = AuctionHouse.validate_price(price)
        self.info("%s", row)


if __name__ == "__main__":
    pass
