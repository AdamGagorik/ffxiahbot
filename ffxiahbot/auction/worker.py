import contextlib
from collections.abc import Iterator
from typing import Any

import sqlalchemy.orm

from ffxiahbot.database import Database


class Worker:
    """
    Base class for Auction House objects.

    :param db: database object
    """

    def __init__(self, db: Database, rollback: bool = True, fail: bool = False) -> None:
        super().__init__()
        if not isinstance(db, Database):
            raise TypeError("expected Database object")
        self._rollback = bool(rollback)
        self._fail = bool(fail)
        self._db = db

    def session(self, **kwargs: Any) -> sqlalchemy.orm.Session:
        """
        Create database session.
        """
        return self._db.session(**kwargs)

    @contextlib.contextmanager
    def scoped_session(self, **kwargs: Any) -> Iterator:
        """
        Create scoped database session.
        """
        _kwargs = {"rollback": self.rollback, "fail": self.fail}
        _kwargs.update(**kwargs)
        try:
            with self._db.scoped_session(**_kwargs) as session:
                yield session
        finally:
            pass

    @property
    def db(self) -> Database:
        return self._db

    @property
    def rollback(self) -> bool:
        return self._rollback

    @rollback.setter
    def rollback(self, value: bool) -> None:
        self._rollback = bool(value)

    @property
    def fail(self) -> bool:
        return self._fail

    @fail.setter
    def fail(self, value: bool) -> None:
        self._fail = bool(value)
