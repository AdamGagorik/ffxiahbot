from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Any

from pydantic import SecretStr

from ffxiahbot import timeutils
from ffxiahbot.auction.browser import Browser
from ffxiahbot.auction.buyer import Buyer
from ffxiahbot.auction.cleaner import Cleaner
from ffxiahbot.auction.seller import Seller
from ffxiahbot.auction.worker import Worker
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
        """
        logger.info("blacklisting: row=%d", rowid)
        self.blacklist.add(rowid)

    def buy_items(self, itemdata: ItemList) -> None:
        """
        The main buy item loop.
        """
        with self.scoped_session(fail=self.fail) as session:
            # find rows that are still up for sale
            q = session.query(AuctionHouse).filter(
                AuctionHouse.seller != self.seller.seller,
                AuctionHouse.sell_date == 0,
                AuctionHouse.sale == 0,
            )
            # loop rows
            for row in q:
                with capture(fail=self.fail):
                    # skip blacklisted rows
                    if row.id not in self.blacklist:
                        # get item data
                        try:
                            data = itemdata[row.itemid]
                        except KeyError:
                            logger.error("item missing from database: %d", row.itemid)
                            data = None

                        if data is not None:
                            # buy stacks
                            if row.stack:
                                # check permissions
                                if data.buy_stacks:
                                    # check price
                                    if row.price <= data.price_stacks:
                                        date = timeutils.timestamp(datetime.datetime.now())
                                        self.buyer.set_row_buyer_info(row, date, data.price_stacks)
                                    else:
                                        logger.info(
                                            "price too high! itemid=%d %d <= %d",
                                            row.itemid,
                                            row.price,
                                            data.price_stacks,
                                        )
                                        self.add_to_blacklist(row.id)
                                else:
                                    logger.debug("not allowed to buy item! itemid=%d", row.itemid)
                                    self.add_to_blacklist(row.id)
                            # buy singles
                            else:
                                # check permissions
                                if data.buy_single:
                                    # check price
                                    if row.price <= data.price_single:
                                        date = timeutils.timestamp(datetime.datetime.now())
                                        self.buyer.set_row_buyer_info(row, date, data.price_single)
                                    else:
                                        logger.info(
                                            "price too high! itemid=%d %d <= %d",
                                            row.itemid,
                                            row.price,
                                            data.price_single,
                                        )
                                        self.add_to_blacklist(row.id)
                                else:
                                    logger.debug("not allowed to buy item! itemid=%d", row.itemid)
                                    self.add_to_blacklist(row.id)
                        else:
                            # item data missing
                            self.add_to_blacklist(row.id)
                    else:
                        # row was blacklisted
                        logger.debug("skipping row %d", row.id)

    def restock_items(self, itemdata: ItemList) -> None:
        """
        The main restock loop.
        """
        # loop over items
        for data in itemdata.items.values():
            # singles
            if data.sell_single:
                # check history
                history_price = self.browser.get_price(itemid=data.itemid, stack=False, seller=self.seller.seller)

                # set history
                if history_price is None or history_price <= 0:
                    now = timeutils.timestamp(datetime.datetime(2099, 1, 1))
                    self.seller.set_history(itemid=data.itemid, stack=False, price=data.price_single, date=now, count=1)

                # get stock
                stock = self.browser.get_stock(itemid=data.itemid, stack=False, seller=self.seller.seller)

                # restock
                while stock < data.stock_single:
                    now = timeutils.timestamp(datetime.datetime(2099, 1, 1))
                    self.seller.sell_item(itemid=data.itemid, stack=False, date=now, price=data.price_single, count=1)
                    stock += 1

            # stacks
            if data.sell_stacks:
                # check history
                history_price = self.browser.get_price(itemid=data.itemid, stack=True, seller=self.seller.seller)

                # set history
                if history_price is None or history_price <= 0:
                    now = timeutils.timestamp(datetime.datetime(2099, 1, 1))
                    self.seller.set_history(itemid=data.itemid, stack=True, price=data.price_stacks, date=now, count=1)

                # get stock
                stock = self.browser.get_stock(itemid=data.itemid, stack=True, seller=self.seller.seller)

                # restock
                while stock < data.stock_stacks:
                    now = timeutils.timestamp(datetime.datetime(2099, 1, 1))
                    self.seller.sell_item(itemid=data.itemid, stack=True, date=now, price=data.price_stacks, count=1)
                    stock += 1
