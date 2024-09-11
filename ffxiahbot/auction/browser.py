from collections.abc import Callable
from typing import Any

import sqlalchemy

from ffxiahbot.auction.worker import Worker
from ffxiahbot.database import Database
from ffxiahbot.logutils import capture
from ffxiahbot.tables.auctionhouse import AuctionHouse


class Browser(Worker):
    """
    Auction House browser.

    Args:
        db: The database object.
    """

    def __init__(self, db: Database, **kwargs: Any) -> None:
        super().__init__(db, **kwargs)

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
    ) -> int:
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
                    session.query(func(AuctionHouse.price))
                    .filter(
                        AuctionHouse.itemid == AuctionHouse.validate_itemid(itemid),
                        AuctionHouse.stack == AuctionHouse.validate_stack(stack),
                        AuctionHouse.sale != 0,
                    )
                    .scalar()
                )
                return int(n)

            # consider seller
            else:
                n = (
                    session.query(func(AuctionHouse.price))
                    .filter(
                        AuctionHouse.itemid == AuctionHouse.validate_itemid(itemid),
                        AuctionHouse.seller == AuctionHouse.validate_seller(seller),
                        AuctionHouse.stack == AuctionHouse.validate_stack(stack),
                        AuctionHouse.sale != 0,
                    )
                    .scalar()
                )
                return int(n)
