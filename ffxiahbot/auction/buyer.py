from dataclasses import dataclass

from ffxiahbot.auction.worker import Worker
from ffxiahbot.logutils import logger
from ffxiahbot.tables.auctionhouse import AuctionHouse


@dataclass(frozen=True)
class Buyer(Worker):
    """
    Auction House buyer.

    Args:
        buyer_name: The name of the character buying the item.
    """

    #: The name of the character buying the item.
    buyer_name: str

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
