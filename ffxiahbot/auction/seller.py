from ffxiahbot.auction.worker import Worker
from ffxiahbot.tables.auctionhouse import AuctionHouse


class Seller(Worker):
    """
    Auction House seller.

    :param db: database object
    :param seller: auction house seller id
    :param seller_name: auction house seller name
    """

    def __init__(self, db, seller=0, seller_name="Zissou", **kwargs):
        super().__init__(db, **kwargs)
        self.seller = int(seller)
        self.seller_name = str(seller_name)

    def set_history(self, itemid, stack, price, date, count=1):
        """
        Set the history of a particular item.

        :param itemid: item number
        :param stack: stack 0|1
        :param date: timestamp
        :param price: price
        :param count: rows
        """
        with self.capture(fail=self.fail):
            itemid = AuctionHouse.validate_itemid(itemid)
            stack = AuctionHouse.validate_stack(stack)
            price = AuctionHouse.validate_price(price)
            date = AuctionHouse.validate_date(date)

            # add row
            with self.scopped_session() as session:
                # add the item multiple times
                for _i in range(count):
                    row = AuctionHouse(
                        itemid=itemid,
                        stack=stack,
                        seller=self.seller,
                        seller_name=self.seller_name,
                        date=date,
                        price=price,
                        buyer_name=self.seller_name,
                        sale=price,
                        sell_date=date,
                    )

                    session.add(row)

    def sell_item(self, itemid, stack, date, price, count):
        """
        Put up a particular item for sale.

        :param itemid: item number
        :param stack: stack 0|1
        :param date: timestamp
        :param price: price
        :param count: rows
        """
        with self.capture(fail=self.fail):
            itemid = AuctionHouse.validate_itemid(itemid)
            stack = AuctionHouse.validate_stack(stack)
            price = AuctionHouse.validate_price(price)
            date = AuctionHouse.validate_date(date)

            # add row
            with self.scopped_session() as session:
                # add the item multiple times
                for _i in range(count):
                    row = AuctionHouse(
                        itemid=itemid,
                        stack=stack,
                        seller=self.seller,
                        seller_name=self.seller_name,
                        date=date,
                        price=price,
                    )

                    session.add(row)


if __name__ == "__main__":
    pass
