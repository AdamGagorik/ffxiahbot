"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import pydarkstar.darkobject
import pydarkstar.database
import contextlib

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

    def session(self, *args, **kwargs):
        """
        Create database session.
        """
        return self._db.session(*args, **kwargs)

    @contextlib.contextmanager
    def scopped_session(self, **kwargs):
        """
        Create scoped database session.
        """
        _kwargs = dict(rollback=self.rollback, fail=self.fail)
        _kwargs.update(**kwargs)
        try:
            with self._db.scoped_session(**_kwargs) as session:
                yield session
        finally:
            pass

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

    @staticmethod
    def validate_itemid(itemid):
        itemid = int(itemid)
        assert itemid > 0
        return itemid

    @staticmethod
    def validate_stack(stack):
        if stack:
            return 1
        return 0

    @staticmethod
    def validate_date(date):
        return pydarkstar.timeutils.timestamp(date)

    @staticmethod
    def validate_price(price):
        price = int(price)
        assert price > 0
        return price

if __name__ == '__main__':
    pass