from __future__ import annotations

import datetime
import random
from dataclasses import asdict, dataclass
from string import ascii_letters
from typing import Any

import pandas as pd

from ffxiahbot.database import Database
from ffxiahbot.tables.auctionhouse import AuctionHouse
from ffxiahbot.timeutils import datetime_to_timestamp

RANDOMIZE: object = object()


def randomdt(
    month=None,
    day=None,
    year=None,
    hour=None,
    minute=None,
    second=None,
    microsecond=None,
    tzinfo=datetime.UTC,
    month_range=(1, 12),
    day_range=(1, 31),
    year_range=(1970, 2000),
    hour_range=(0, 23),
    minute_range=(0, 59),
    second_range=(0, 59),
    microsecond_range=(0, 0),
):
    """
    Create a random datetime object.
    """
    if month is None:
        month = random.randint(*month_range)

    if day is None:
        day = random.randint(*day_range)

    if year is None:
        year = random.randint(*year_range)

    if hour is None:
        hour = random.randint(*hour_range)

    if minute is None:
        minute = random.randint(*minute_range)

    if second is None:
        second = random.randint(*second_range)

    if microsecond is None:
        microsecond = random.randint(*microsecond_range)

    for i in range(3):
        try:
            return datetime.datetime(year, month, day - i, hour, minute, second, microsecond, tzinfo)
        except ValueError:
            pass

    return datetime.datetime(year, month, day - 3, hour, minute, second, microsecond, tzinfo)


@dataclass
class AuctionHouseRowBuilder:
    """
    A class to build a row for the AuctionHouse table.
    """

    itemid: int | None | type[RANDOMIZE] = RANDOMIZE
    stack: int | None | type[RANDOMIZE] = RANDOMIZE
    seller: int | None | type[RANDOMIZE] = RANDOMIZE
    seller_name: str | None | type[RANDOMIZE] = RANDOMIZE
    date: int | None | type[RANDOMIZE] = RANDOMIZE
    price: int | None | type[RANDOMIZE] = RANDOMIZE
    buyer_name: str | None | type[RANDOMIZE] = None
    sale: int | None | type[RANDOMIZE] = 0
    sell_date: int | None | type[RANDOMIZE] = None

    @classmethod
    def many(cls, count: int, **kwargs: Any) -> tuple[AuctionHouseRowBuilder, ...]:
        return tuple(cls(**kwargs) for _ in range(count))

    def __post_init__(self):
        self.itemid = self._make_random_int(self.itemid, 0, 2**16 - 1)
        self.stack = self._make_random_int(self.stack, 0, 1)
        self.seller = self._make_random_int(self.seller, 0, 2**32 - 1)
        self.seller_name = self._make_random_str(self.seller_name, 15)
        self.date = self._make_random_date(self.date)
        self.price = self._make_random_int(self.price, 0, 2**32 - 1)
        self.buyer_name = self._make_random_str(self.buyer_name, 15)
        self.sale = self._make_random_int(self.sale, 0, 2**32 - 1)
        self.sell_date = self._make_random_date(self.sell_date)

    def make_orm_object(self) -> AuctionHouse:  # noqa: C901
        def _():
            if self.itemid is not None:
                yield "itemid", AuctionHouse.validate_itemid(self.itemid)
            if self.stack is not None:
                yield "stack", AuctionHouse.validate_stack(self.stack)
            if self.seller is not None:
                yield "seller", AuctionHouse.validate_seller(self.seller)
            if self.seller_name is not None:
                yield "seller_name", AuctionHouse.validate_seller_name(self.seller_name)
            if self.date is not None:
                yield "date", AuctionHouse.validate_date(self.date)
            if self.price is not None:
                yield "price", AuctionHouse.validate_price(self.price)
            if self.buyer_name is not None:
                yield "buyer_name", AuctionHouse.validate_buyer_name(self.buyer_name)
            if self.sale is not None:
                yield "sale", AuctionHouse.validate_sale(self.sale)
            if self.sell_date is not None:
                yield "sell_date", AuctionHouse.validate_sell_date(self.sell_date)

        return AuctionHouse(**dict(_()))

    def add_item_for_sale(self, db: Database) -> None:
        with db.scoped_session() as session:
            session.add(self.make_orm_object())

    @classmethod
    def add_items_for_sale(cls, db: Database, *items: AuctionHouseRowBuilder) -> None:
        for item in items:
            item.add_item_for_sale(db)

    def validate_query_result(self, row: AuctionHouse, **kwargs: Any) -> None:
        if "id" in kwargs:
            assert row.id == kwargs.pop("id")

        assert row.itemid == kwargs.pop("itemid", self.itemid)
        assert row.stack == kwargs.pop("stack", self.stack)
        assert row.seller == kwargs.pop("seller", self.seller)
        assert row.seller_name == kwargs.pop("seller_name", self.seller_name)
        assert row.date == kwargs.pop("date", self.date)
        assert row.price == kwargs.pop("price", self.price)
        assert row.buyer_name == kwargs.pop("buyer_name", self.buyer_name)
        assert row.sale == kwargs.pop("sale", self.sale if self.sale is not None else 0)
        assert row.sell_date == kwargs.pop("sell_date", self.sell_date if self.sell_date is not None else 0)

    @staticmethod
    def _make_random_int(value: int | None | type[RANDOMIZE], lo: int, hi: int) -> int | None:
        return value if value is not RANDOMIZE else random.randint(lo, hi)

    @staticmethod
    def _make_random_str(value: str | None | type[RANDOMIZE], size: int) -> str | None:
        return value if value is not RANDOMIZE else str("".join(random.choices(ascii_letters, k=size)))

    @staticmethod
    def _make_random_date(value: int | None | type[RANDOMIZE]) -> int | None:
        return value if value is not RANDOMIZE else datetime_to_timestamp(randomdt())


DTYPES = {
    "itemid": "uint32",
    "stack": "uint8",
    "seller": "uint32",
    "seller_name": "string",
    "date": "uint32",
    "price": "uint32",
    "buyer_name": "string",
    "sale": "UInt32",
    "sell_date": "UInt32",
}


def setup_ah_transactions(db: Database, *transactions: AuctionHouseRowBuilder) -> pd.DataFrame:
    AuctionHouseRowBuilder.add_items_for_sale(db, *transactions)
    frame = pd.DataFrame([asdict(t) for t in transactions]).astype(DTYPES)
    frame["builder"] = transactions
    return frame


#
# @dataclass
# class Seller:
#     seller: int
#     seller_name: str
#     sold_stacks: dict[int, int] = field(default_factory=dict)
#     sold_singles: dict[int, int] = field(default_factory=dict)
#     selling_stacks: dict[int, int] = field(default_factory=dict)
#     selling_singles: dict[int, int] = field(default_factory=dict)
#     sold_stacks_builders_objects: dict[int, tuple[AuctionHouseRowBuilder, ...]] = field(default_factory=dict)
#     sold_singles_builders_objects: dict[int, tuple[AuctionHouseRowBuilder, ...]] = field(default_factory=dict)
#     selling_stacks_builders_objects: dict[int, tuple[AuctionHouseRowBuilder, ...]] = field(default_factory=dict)
#     selling_singles_builders_objects: dict[int, tuple[AuctionHouseRowBuilder, ...]] = field(default_factory=dict)
#
#
# @dataclass
# class ItemInfo:
#     total: int
#     min_price: int
#     max_price: int
#
#
# @dataclass
# class ItemInfos:
#     ids: set[int]
#     sold: dict[int, ItemInfo]
#     selling: dict[int, ItemInfo]
#
#
# def setup_ah_sales(db: Database, *sellers: Seller) -> ItemInfos:
#     known_itemids: set[int] = set()
#     sold_stacks_total: Counter[int] = Counter()
#     sold_singles_total: Counter[int] = Counter()
#     selling_stacks_total: Counter[int] = Counter()
#     selling_singles_total: Counter[int] = Counter()
#
#     for seller in sellers:
#         # put of stacks for sale
#         for itemid, count in seller.selling_stacks.items():
#             seller.selling_stacks_builders_objects[itemid] = AuctionHouseRowBuilder.many(
#                 count,
#                 db=db,
#                 seller=seller.seller,
#                 seller_name=seller.seller_name,
#                 itemid=itemid,
#                 stack=1,
#             )
#             known_itemids.add(itemid)
#             selling_stacks_total[itemid] += count
#
#         # put of singles for sale
#         for itemid, count in seller.selling_singles.items():
#             seller.selling_singles_builders_objects[itemid] = AuctionHouseRowBuilder.many(
#                 count,
#                 db=db,
#                 seller=seller.seller,
#                 seller_name=seller.seller_name,
#                 itemid=itemid,
#                 stack=0,
#             )
#             known_itemids.add(itemid)
#             selling_singles_total[itemid] += count
#
#         # add history of stacks sold
#         for itemid, count in seller.sold_stacks.items():
#             seller.sold_stacks_builders_objects[itemid] = AuctionHouseRowBuilder.many(
#                 count,
#                 db=db,
#                 seller=seller.seller,
#                 seller_name=seller.seller_name,
#                 itemid=itemid,
#                 stack=1,
#                 buyer_name=RANDOMIZE,
#                 sale=RANDOMIZE,
#                 sell_date=RANDOMIZE,
#             )
#             known_itemids.add(itemid)
#             sold_stacks_total[itemid] += count
#
#         # add history of singles sold
#         for itemid, count in seller.sold_singles.items():
#             seller.sold_singles_builders_objects[itemid] = AuctionHouseRowBuilder.many(
#                 count,
#                 db=db,
#                 seller=seller.seller,
#                 seller_name=seller.seller_name,
#                 itemid=itemid,
#                 stack=0,
#                 buyer_name=RANDOMIZE,
#                 sale=RANDOMIZE,
#                 sell_date=RANDOMIZE,
#             )
#             known_itemids.add(itemid)
#             sold_singles_total[itemid] += count
#
#         return known_itemids, sold_stacks_total, sold_singles_total, selling_stacks_total, selling_singles_total
