from __future__ import annotations

import datetime
import random
from collections import Counter
from dataclasses import dataclass
from typing import Any

import pandas as pd
from pydantic import SecretStr

from ffxiahbot import timeutils
from ffxiahbot.auction.browser import Browser
from ffxiahbot.auction.buyer import Buyer
from ffxiahbot.auction.cleaner import Cleaner
from ffxiahbot.auction.seller import Seller
from ffxiahbot.auction.worker import Worker
from ffxiahbot.common import progress_bar
from ffxiahbot.database import Database
from ffxiahbot.itemlist import ItemList
from ffxiahbot.logutils import capture, logger
from ffxiahbot.tables.auctionhouse import AuctionHouse


@dataclass(frozen=True)
class Manager(Worker):
    """
    Auction House browser.
    """

    #: Auction House database row ids to ignore.
    blacklist: set[int]
    #: A worker to browse the auction house.
    browser: Browser
    #: A worker to clean the auction house.
    cleaner: Cleaner
    #: A worker to sell and restock items.
    seller: Seller
    #: A worker to purchase items.
    buyer: Buyer

    @classmethod
    def create_database_and_manager(
        cls,
        hostname: str,
        database: str,
        username: str,
        password: str | SecretStr,
        port: int,
        **kwargs: Any,
    ) -> Manager:
        """
        Create database and manager at the same time.

        Args:
            hostname: Database hostname.
            database: Database name.
            username: Database username.
            password: Database password.
            port: Database port.
            **kwargs: Additional arguments passed to the `Manager.from_db` method.
        """
        # connect to database
        db = Database.pymysql(
            hostname=hostname,
            database=database,
            username=username,
            password=password if isinstance(password, str) else password.get_secret_value(),
            port=port,
        )

        # create auction house manager
        return cls.from_db(db=db, **kwargs)

    @classmethod
    def from_db(
        cls,
        db: Database,
        name: str,
        fail: bool = True,
        rollback: bool = True,
        blacklist: set[int] | None = None,
    ) -> Manager:
        """
        Create manager from database.

        Args:
            db: Database connection.
            name: Name of the seller and buyer.
            fail: If True, raise exceptions.
            rollback: If True, rollback transactions.
            blacklist: Auction House row ids to ignore.
        """
        return cls(
            db=db,
            blacklist=blacklist if blacklist is not None else set(),
            browser=Browser(db=db, rollback=rollback, fail=fail),
            cleaner=Cleaner(db=db, rollback=rollback, fail=fail),
            seller=Seller(db=db, rollback=rollback, fail=fail, seller=0, seller_name=name),
            buyer=Buyer(db=db, rollback=rollback, fail=fail, buyer_name=name),
            rollback=rollback,
            fail=fail,
        )

    def add_to_blacklist(self, rowid: int) -> None:
        """
        Add row to blacklist.

        Args:
            rowid: Row id to blacklist.
        """
        logger.info("blacklisting: row=%d", rowid)
        self.blacklist.add(rowid)

    def buy_items(self, item_list: ItemList, use_buying_rates: bool = False) -> None:  # noqa: C901
        """
        The main buy item loop.

        Args:
            item_list: Item data.
            use_buying_rates: If True, only buy items at their buying rate.
        """
        with self.scoped_session(fail=self.fail) as session:
            # find rows that are still up for sale
            q = session.query(AuctionHouse).filter(
                AuctionHouse.seller != self.seller.seller,
                AuctionHouse.sell_date == 0,
                AuctionHouse.sale == 0,
            )
            # loop rows
            counts: Counter[str] = Counter()
            for row in q:
                if row.id in self.blacklist:
                    logger.debug("skipping blacklisted row %d", row.id)
                    counts["blacklisted"] += 1
                    continue

                if row.itemid not in item_list:
                    logger.error("item missing from database: %d", row.itemid)
                    self.add_to_blacklist(row.id)
                    counts["unknown itemid"] += 1
                    continue

                with capture(fail=self.fail):
                    item = item_list[row.itemid]

                    if row.stack:
                        if not item.buy_stacks:
                            logger.debug("not allowed to buy item! itemid=%d", row.itemid)
                            self.add_to_blacklist(row.id)
                            counts["forbidden item"] += 1
                        else:
                            if not use_buying_rates or random.random() <= item.buy_rate_stacks:
                                if self._buy_row(row, item.price_stacks):
                                    counts["stack purchased"] += 1
                                else:
                                    counts["price too high"] += 1
                            else:
                                counts["buy rate too low"] += 1
                    else:
                        if not item.buy_single:
                            logger.debug("not allowed to buy item! itemid=%d", row.itemid)
                            self.add_to_blacklist(row.id)
                            counts["forbidden item"] += 1
                        else:
                            if not use_buying_rates or random.random() <= item.buy_rate_single:
                                if self._buy_row(row, item.price_single):
                                    counts["single purchased"] += 1
                                else:
                                    counts["price too high"] += 1
                            else:
                                counts["buy rate too low"] += 1

            counts_frame = pd.DataFrame.from_dict(counts, orient="index").rename(columns={0: "count"})
            if not counts_frame.empty:
                logger.debug("manager.buy_items counts: \n%s", counts_frame)
            else:
                logger.warning("no rows processed when buying items (no items for sale?)")

    def _buy_row(self, row: AuctionHouse, max_price: int) -> bool:
        """
        Buy a row.

        Args:
            row: Auction House row to buy.
            max_price: Maximum price to pay.
        """
        if max_price <= 0:
            logger.error("max buying price is zero! itemid=%d", row.itemid)
            self.add_to_blacklist(row.id)
            return False

        # check price
        if row.price <= max_price:
            date = timeutils.timestamp(datetime.datetime.now())
            self.buyer.set_row_buyer_info(row, date, max_price)
            return True
        else:
            logger.info(
                "price too high! itemid=%d %d <= %d",
                row.itemid,
                row.price,
                max_price,
            )
            self.add_to_blacklist(row.id)
            return False

    def restock_items(self, item_list: ItemList, use_selling_rates: bool = False) -> None:
        """
        The main restock loop.

        Args:
            item_list: Item data.
            use_selling_rates: If True, only restock items at their selling rate.
        """
        # loop over items
        with progress_bar("[red]Restocking Items...", total=len(item_list)) as (progress, task):
            for item in item_list.items.values():
                # singles
                if item.sell_single and item.price_single > 0:
                    self._sell_item(
                        item.itemid,
                        stack=False,
                        price=item.price_single,
                        stock=item.stock_single,
                        rate=None if not use_selling_rates else item.sell_rate_single,
                    )
                    progress.update(task, advance=0.5)

                # stacks
                if item.sell_stacks and item.price_stacks > 0:
                    self._sell_item(
                        item.itemid,
                        stack=True,
                        price=item.price_stacks,
                        stock=item.stock_stacks,
                        rate=None if not use_selling_rates else item.sell_rate_stacks,
                    )
                    progress.update(task, advance=0.5)

    @property
    def _sell_time(self) -> int:
        """
        The timestamp to use for selling items.
        """
        return timeutils.timestamp(datetime.datetime(2099, 1, 1))

    def _sell_item(self, itemid: int, stack: bool, price: int, stock: int, rate: float | None) -> None:
        """
        Sell an item.

        Args:
            itemid: The item id.
            stack: True if selling stacks, False if selling singles.
            price: The price to sell the item for.
            stock: The amount of items to stock.
        """
        # check history
        history_price = self.browser.get_price(itemid=itemid, stack=stack, seller=self.seller.seller)

        # set history
        if history_price is None or history_price <= 0:
            self.seller.set_history(itemid=itemid, stack=stack, price=price, date=self._sell_time, count=1)

        # get stock
        current_stock = self.browser.get_stock(itemid=itemid, stack=stack, seller=self.seller.seller)

        # restock
        if current_stock < stock:
            for _ in range(stock - current_stock):
                if rate is None or random.random() <= rate:
                    self.seller.sell_item(itemid=itemid, stack=stack, date=self._sell_time, price=price, count=1)
