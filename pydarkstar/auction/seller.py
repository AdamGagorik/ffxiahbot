"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import pydarkstar.darkobject
import pydarkstar.database

class Seller(pydarkstar.darkobject.DarkObject):
    """
    Buyer/Seller

    :param db: database object
    :param seller: auction house seller id
    :param seller_name: auction house seller name
    """
    def __init__(self, db, seller=0, seller_name='Zissou', *args, **kwargs):
        super(Seller, self).__init__(*args, **kwargs)
        assert isinstance(db, pydarkstar.database.Database)
        self.db = db
        self.seller = int(seller)
        self.seller_name = str(seller_name)

if __name__ == '__main__':
    pass