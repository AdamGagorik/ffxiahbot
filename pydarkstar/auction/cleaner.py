"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import pydarkstar.auction.auctionbase
import pydarkstar.database

class Cleaner(pydarkstar.auction.auctionbase.AuctionBase):
    """
    Auction House cleaner.

    :param db: database object
    """
    def __init__(self, db, *args, **kwargs):
        super(Cleaner, self).__init__(db, *args, **kwargs)

if __name__ == '__main__':
    pass