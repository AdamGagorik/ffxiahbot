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
    def __init__(self, db, rollback=True, fail=False, *args, **kwargs):
        super(AuctionBase, self).__init__(*args, **kwargs)
        assert isinstance(db, pydarkstar.database.Database)
        self._rollback = bool(rollback)
        self._fail = bool(fail)
        self._db = db

    @property
    def db(self):
        return self._db

    @property
    def rollback(self):
        return self._rollback
    @rollback.setter
    def rollback(self, value):
        self._rollback = bool(value)

    @property
    def fail(self):
        return self._fail
    @fail.setter
    def fail(self, value):
        self._fail = bool(value)

if __name__ == '__main__':
    pass