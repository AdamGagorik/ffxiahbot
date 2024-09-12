from collections.abc import Callable
from dataclasses import dataclass

import sqlalchemy

from ffxiahbot.auction.worker import Worker
from ffxiahbot.logutils import capture
from ffxiahbot.tables.auctionhouse import AuctionHouse


@dataclass(frozen=True)
class Browser(Worker):
    """
    Auction House browser.
    """

    def count(self) -> int:
        """
        Get the number of rows.
        """
        with self.scoped_session() as session:
            return int(session.query(AuctionHouse).count())

    def get_stock(self, itemid: int, stack: bool = False, seller: int | None = None) -> int:
        """
        Get stock of an item.

        Args:
            itemid: The item number.
            stack: Consider stacks?
            seller: Consider seller?

        Returns:
            The total number of singles or stacks being sold, in general or by the specific seller.
        """
        with capture(fail=self.fail), self.scoped_session() as session:
            # ignore seller
            if seller is None:
                n = (
                    session.query(AuctionHouse)
                    .filter(
                        AuctionHouse.itemid == AuctionHouse.validate_itemid(itemid),
                        AuctionHouse.stack == AuctionHouse.validate_stack(stack),
                        AuctionHouse.sale == 0,
                    )
                    .count()
                )
                return int(n)

            # consider seller
            else:
                n = (
                    session.query(AuctionHouse)
                    .filter(
                        AuctionHouse.itemid == AuctionHouse.validate_itemid(itemid),
                        AuctionHouse.seller == AuctionHouse.validate_seller(seller),
                        AuctionHouse.stack == AuctionHouse.validate_stack(stack),
                        AuctionHouse.sale == 0,
                    )
                    .count()
                )
                return int(n)

    def get_price(
        self, itemid: int, stack: bool = False, seller: int | None = None, func: Callable = sqlalchemy.func.min
    ) -> int | None:
        """
        Get the historical price of an item.

        Args:
            itemid: The item number.
            stack: Consider stacks?
            seller: Consider seller?
            func: Aggregation function (min).

        Return:
            The aggregated priced for an item, in general or for the specific seller.
        """
        with capture(fail=self.fail), self.scoped_session() as session:
            # ignore seller
            if seller is None:
                n = (
                    session.query(func(AuctionHouse.sale))
                    .filter(
                        AuctionHouse.itemid == AuctionHouse.validate_itemid(itemid),
                        AuctionHouse.stack == AuctionHouse.validate_stack(stack),
                        AuctionHouse.sale != 0,
                    )
                    .scalar()
                )
                return None if n is None else int(n)

            # consider seller
            else:
                n = (
                    session.query(func(AuctionHouse.sale))
                    .filter(
                        AuctionHouse.itemid == AuctionHouse.validate_itemid(itemid),
                        AuctionHouse.seller == AuctionHouse.validate_seller(seller),
                        AuctionHouse.stack == AuctionHouse.validate_stack(stack),
                        AuctionHouse.sale != 0,
                    )
                    .scalar()
                )
                return None if n is None else int(n)
