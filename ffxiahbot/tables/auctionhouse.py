from sqlalchemy import text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from ffxiahbot import timeutils
from ffxiahbot.tables.base import Base

_template = """
[AuctionHouseRow]
    addr        = {addr}
    id          = {self.id}
    itemid      = {self.itemid}
    stack       = {self.stack}
    seller      = {self.seller}
    seller_name = {self.seller_name}
    date        = {self.date}
    price       = {self.price}
    buyer_name  = {self.buyer_name}
    sale        = {self.sale}
    sell_date   = {self.sell_datestr}
"""[:-1]


class AuctionHouse(Base):
    __tablename__ = "auction_house"

    id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False, autoincrement=True, primary_key=True)
    itemid: Mapped[int] = mapped_column(
        SMALLINT(5, unsigned=True), nullable=False, index=True, server_default=text("'0'")
    )
    stack: Mapped[int] = mapped_column(TINYINT(1, unsigned=True), nullable=False, server_default=text("'0'"))
    seller: Mapped[int] = mapped_column(
        INTEGER(10, unsigned=True), nullable=False, index=True, server_default=text("'0'")
    )
    seller_name: Mapped[str] = mapped_column(VARCHAR(15), nullable=True)
    date: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False, server_default=text("'0'"))
    price: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False, server_default=text("'0'"))
    buyer_name: Mapped[str] = mapped_column(VARCHAR(15), nullable=True)
    sale: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False, server_default=text("'0'"))
    sell_date: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False, server_default=text("'0'"))

    def __repr__(self) -> str:
        return f"({hex(id(self))}) AuctionHouseRow id={self.id}"

    def __str__(self) -> str:
        return _template.format(self=self, addr=hex(id(self)))

    @staticmethod
    def validate_itemid(itemid: int) -> int:
        itemid = int(itemid)
        if itemid < 0:
            raise ValueError(f"itemid={itemid} is negative")
        return itemid

    @staticmethod
    def validate_stack(stack: int | bool) -> int:
        if stack:
            return 1
        return 0

    @staticmethod
    def validate_seller(seller: int) -> int:
        seller = int(seller)
        if seller < 0:
            raise ValueError(f"seller={seller} is negative")
        return seller

    @staticmethod
    def validate_seller_name(seller_name: str) -> str:
        if len(seller_name) > 15:
            raise ValueError(f"seller_name={seller_name} is too long")
        return seller_name

    @staticmethod
    def validate_date(date: int) -> int:
        stamp = timeutils.timestamp(date)
        if (dt := timeutils.timestamp_to_datetime(stamp)).year < 1970:
            raise ValueError(f"date={dt} is before 1970")
        return stamp

    @staticmethod
    def validate_price(price: int) -> int:
        price = int(price)
        if price < 0:
            raise ValueError(f"price={price} is negative")
        return price

    @staticmethod
    def validate_sale(sale: int) -> int:
        sale = int(sale)
        if sale < 0:
            raise ValueError(f"sale={sale} is negative")
        return sale

    @staticmethod
    def validate_buyer_name(buyer_name: str) -> str:
        if len(buyer_name) > 15:
            raise ValueError(f"buyer_name={buyer_name} is too long")
        return buyer_name

    @staticmethod
    def validate_sell_date(sell_date: int) -> int:
        stamp = timeutils.timestamp(sell_date)
        if (dt := timeutils.timestamp_to_datetime(stamp)).year < 1970:
            raise ValueError(f"sell_date={dt} is before 1970")
        return stamp

    @property
    def sell_datestr(self) -> str:
        if self.sell_date is None:
            return str(None)
        return timeutils.datetime_to_str(timeutils.timestamp_to_datetime(int(self.sell_date)))
