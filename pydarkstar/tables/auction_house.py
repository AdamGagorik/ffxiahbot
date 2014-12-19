"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
from sqlalchemy import Column, Integer, SmallInteger, String, text
from pydarkstar.tables.base import Base

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

if __name__ == '__main__':
    pass