"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
from sqlalchemy import Column, Integer, SmallInteger, String, text
from pydarkstar.tables.base import Base

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
    sell_date   = {self.sell_date}
"""[:-1]

class AuctionHouse(Base):
    __tablename__ = 'auction_house'

    id          = Column(Integer, primary_key=True)
    itemid      = Column(SmallInteger, nullable=False, index=True, server_default=text("'0'"))
    stack       = Column(Integer, nullable=False, server_default=text("'0'"))
    seller      = Column(Integer, nullable=False, server_default=text("'0'"))
    seller_name = Column(String(15))
    date        = Column(Integer, nullable=False, server_default=text("'0'"))
    price       = Column(Integer, nullable=False, server_default=text("'0'"))
    buyer_name  = Column(String(15))
    sale        = Column(Integer, nullable=False, server_default=text("'0'"))
    sell_date   = Column(Integer, nullable=False, server_default=text("'0'"))

    def __repr__(self):
        return '({addr}) AuctionHouseRow id={self.id}'.format(self=self, addr=hex(id(self)))

    def __str__(self):
        return _template.format(self=self, addr=hex(id(self)))

if __name__ == '__main__':
    pass