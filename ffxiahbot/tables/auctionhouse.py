from sqlalchemy import Column, Integer, SmallInteger, String, text
from .base import Base
from .. import timeutils

_template = \
    """
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
    __tablename__ = 'auction_house'

    id = Column(Integer, primary_key=True)
    itemid = Column(SmallInteger, nullable=False, index=True, server_default=text("'0'"))
    stack = Column(Integer, nullable=False, server_default=text("'0'"))
    seller = Column(Integer, nullable=False, server_default=text("'0'"))
    seller_name = Column(String(15))
    date = Column(Integer, nullable=False, server_default=text("'0'"))
    price = Column(Integer, nullable=False, server_default=text("'0'"))
    buyer_name = Column(String(15))
    sale = Column(Integer, nullable=False, server_default=text("'0'"))
    sell_date = Column(Integer, nullable=False, server_default=text("'0'"))

    def __repr__(self):
        return '({addr}) AuctionHouseRow id={self.id}'.format(self=self, addr=hex(id(self)))

    def __str__(self):
        return _template.format(self=self, addr=hex(id(self)))

    @staticmethod
    def validate_itemid(itemid):
        itemid = int(itemid)
        assert itemid > 0
        return itemid

    @staticmethod
    def validate_stack(stack):
        if stack:
            return 1
        return 0

    @staticmethod
    def validate_seller(seller):
        seller = int(seller)
        assert seller >= 0
        return seller

    @staticmethod
    def validate_date(date):
        return timeutils.timestamp(date)

    @staticmethod
    def validate_price(price):
        price = int(price)
        assert price >= 0
        return price

    @property
    def sell_datestr(self):
        if self.sell_date is None:
            return str(None)
        return timeutils.datetime_to_str(timeutils.timestamp_to_datetime(self.sell_date))


if __name__ == '__main__':
    pass
