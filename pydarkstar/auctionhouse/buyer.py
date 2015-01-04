"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import pydarkstar.auctionhouse.auctionbase
import pydarkstar.database

class Buyer(pydarkstar.auctionhouse.auctionbase.AuctionBase):
    """
    Auction House buyer.

    :param db: database object
    """
    def __init__(self, db, *args, **kwargs):
        super(Buyer, self).__init__(db, *args, **kwargs)

if __name__ == '__main__':
    pass