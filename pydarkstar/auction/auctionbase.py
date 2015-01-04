"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import pydarkstar.darkobject
import pydarkstar.database

class AuctionBase(pydarkstar.darkobject.DarkObject):
    """
    Base class for Auction House objects.

    :param db: database object
    """
    def __init__(self, db, *args, **kwargs):
        super(AuctionBase, self).__init__(*args, **kwargs)
        assert isinstance(db, pydarkstar.database.Database)
        self.db = db

if __name__ == '__main__':
    pass