from ..tables.auctionhouse import AuctionHouse
from ..tables.deliverybox import DeliveryBox
from .worker import Worker


class Buyer(Worker):
    """
    Auction House buyer.

    :param db: database object
    """

    def __init__(self, db, buyer_name='Zissou', **kwargs):
        super(Buyer, self).__init__(db, **kwargs)
        self.buyer_name = str(buyer_name)

    def buy_item(self, row, date, price):
        """
        Buy item for given price.
        """
        # validate
        if not row.sale == 0:
            raise RuntimeError('item already sold!')

        
        row.buyer_name = self.buyer_name
        row.sell_date = AuctionHouse.validate_date(date)
        row.sale = AuctionHouse.validate_price(price)
        self.info('%s', row)
        self.scopped_session(fail=self.fail) as session:
            # find rows that are still up for sale
            q = session.query(DeliveryBox).filter(
                DeliveryBox.charname == row.seller_name
            )
        dbox = DeliveryBox(
            charid      = row.seller
            charname    = row.seller_name
            box         = 1
            slot        = q.slot +1
            itemid      = 65535
            itemsubid   = 0
            quantity    = row.sale
            senderid    = 0
            sender      = self.buyer_name
            received    = 0
            sent        = 0
                    )

        session.add(dbox)


if __name__ == '__main__':
    pass
