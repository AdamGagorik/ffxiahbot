from dataclasses import dataclass

from ffxiahbot.auction.worker import Worker
from ffxiahbot.logutils import capture
from ffxiahbot.tables.auctionhouse import AuctionHouse


@dataclass(frozen=True)
class Seller(Worker):
    """
    Auction House seller.

    Args:
        db: The database object.
        seller: The auction house seller id.
        seller_name: The auction house seller name.
    """

    #: The auction house seller id.
    seller: int
    #: The auction house seller name.
    seller_name: str

    def set_history(self, itemid: int, stack: int | bool, price: int, date: int, count: int = 1) -> None:
        """
        Set the history of a particular item.

        Args:
            itemid: The item number.
            stack: The stack size.
            price: The price.
            date: The timestamp.
            count: The number of rows.
        """
        with capture(fail=self.fail):
            itemid = AuctionHouse.validate_itemid(itemid)
            stack = AuctionHouse.validate_stack(stack)
            price = AuctionHouse.validate_price(price)
            date = AuctionHouse.validate_date(date)

            # add row
            with self.scoped_session() as session:
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

    def sell_item(self, itemid: int, stack: int, date: int, price: int, count: int) -> None:
        """
        Put up a particular item for sale.

        Args:
            itemid: The item number.
            stack: The stack size.
            date: The timestamp.
            price: The price.
            count: The number of rows.
        """
        with capture(fail=self.fail):
            itemid = AuctionHouse.validate_itemid(itemid)
            stack = AuctionHouse.validate_stack(stack)
            price = AuctionHouse.validate_price(price)
            date = AuctionHouse.validate_date(date)

            # add row
            with self.scoped_session() as session:
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
