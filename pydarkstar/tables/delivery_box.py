"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
from sqlalchemy import Column, Integer, SmallInteger, String, text
from sqlalchemy.dialects.mysql.base import BIT
from pydarkstar.tables.base import Base

class DeliveryBox(Base):
    __tablename__ = 'delivery_box'

    charid    = Column(Integer, primary_key=True, nullable=False)
    charname  = Column(String(15))
    box       = Column(Integer, primary_key=True, nullable=False)
    slot      = Column(Integer, primary_key=True, nullable=False, server_default=text("'0'"))
    itemid    = Column(SmallInteger, nullable=False)
    itemsubid = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    quantity  = Column(Integer, nullable=False)
    senderid  = Column(Integer, nullable=False, server_default=text("'0'"))
    sender    = Column(String(15))
    received  = Column(BIT(1), nullable=False)
    sent      = Column(BIT(1), nullable=False)

if __name__ == '__main__':
    pass