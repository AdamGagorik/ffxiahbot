from sqlalchemy import Column, Integer, SmallInteger, String, text
from sqlalchemy.dialects.mysql.base import BIT

from ffxiahbot.tables.base import Base

_template = """
[DeliveryBoxRow]
    charid      = {self.charid}
    charname    = {self.charname}
    box         = {self.box}
    slot        = {self.slot}
    itemid      = {self.itemid}
    itemsubid   = {self.itemsubid}
    quantity    = {self.quantity}
    senderid    = {self.senderid}
    sender      = {self.sender}
    received    = {self.received}
    sent        = {self.sent}
"""[:-1]


class DeliveryBox(Base):
    __tablename__ = "delivery_box"

    charid = Column(Integer, primary_key=True, nullable=False)
    charname = Column(String(15))
    box = Column(Integer, primary_key=True, nullable=False)
    slot = Column(Integer, primary_key=True, nullable=False, server_default=text("'0'"))
    itemid = Column(SmallInteger, nullable=False)
    itemsubid = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    quantity = Column(Integer, nullable=False)
    senderid = Column(Integer, nullable=False, server_default=text("'0'"))
    sender = Column(String(15))
    received = Column(BIT(1), nullable=False)
    sent = Column(BIT(1), nullable=False)

    def __repr__(self):
        return f"({hex(id(self))}) DeliveryBoxRow charid={self.charid}"

    def __str__(self):
        return _template.format(self=self, addr=hex(id(self)))


if __name__ == "__main__":
    pass
