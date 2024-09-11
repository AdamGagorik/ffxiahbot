from typing import Any

from ffxiahbot.auction.worker import Worker
from ffxiahbot.database import Database
from ffxiahbot.logutils import logger
from ffxiahbot.tables.auctionhouse import AuctionHouse


class Buyer(Worker):
    """
    Auction House buyer.

    Args:
        db: The database object.
    """

    def __init__(self, db: Database, buyer_name: str = "Zissou", **kwargs: Any) -> None:
        super().__init__(db, **kwargs)
        self.buyer_name = str(buyer_name)

    def set_row_buyer_info(self, row: AuctionHouse, date: int, price: int) -> None:
        """
        Update the AuctionHouse row with buyer information.
        This does not actually buy the item unless a database commit is made.

        Args:
            row: The AuctionHouse row.
            date: The date of the sale.
            price: The price of the sale.
        """
        # validate
        if row.sale != 0:
            raise RuntimeError("item not for sale!")

        row.buyer_name = AuctionHouse.validate_buyer_name(self.buyer_name)
        row.sell_date = AuctionHouse.validate_date(date)
        row.sale = AuctionHouse.validate_price(price)
        logger.info("%s", row)
