"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import pydarkstar.darkobject
import pydarkstar.database

class Seller(pydarkstar.darkobject.DarkObject):
    """
    Buyer/Seller

    :param db: database object
    """
    def __init__(self, db, *args, **kwargs):
        super(Seller, self).__init__(*args, **kwargs)
        assert isinstance(db, pydarkstar.database.Database)
        self.db = db

if __name__ == '__main__':
    pass