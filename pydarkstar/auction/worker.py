from ..darkobject import DarkObject
from ..database import Database
import contextlib


class Worker(DarkObject):
    """
    Base class for Auction House objects.

    :param db: database object
    """

    def __init__(self, db, rollback=True, fail=False):
        super(Worker, self).__init__()
        assert isinstance(db, Database)
        self._rollback = bool(rollback)
        self._fail = bool(fail)
        self._db = db

    def session(self, **kwargs):
        """
        Create database session.
        """
        return self._db.session(**kwargs)

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


if __name__ == '__main__':
    pass
