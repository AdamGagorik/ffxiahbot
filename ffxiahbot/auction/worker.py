import contextlib
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any

import sqlalchemy.orm
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from ffxiahbot.database import Database


@dataclass(frozen=True)
class Worker:
    """
    Base class for Auction House objects.

    Args:
        db: The database object.
    """

    #: The database object.
    db: Database
    #: Should the session fail on error?
    fail: bool
    #: Should the session rollback on error?
    rollback: bool

    def session(self, **kwargs: Any) -> sqlalchemy.orm.Session:
        """
        Create database session.
        """
        return self.db.session(**kwargs)

    @contextlib.contextmanager
    def scoped_session(self, **kwargs: Any) -> Iterator:
        """
        Create scoped database session.
        """
        _kwargs = {"rollback": self.rollback, "fail": self.fail}
        _kwargs.update(**kwargs)
        try:
            with self.db.scoped_session(**_kwargs) as session:
                yield session
        finally:
            pass

    def can_connect(self) -> bool:
        """
        Test database connection.
        """
        try:
            with self.scoped_session(fail=True) as session:
                session.execute(text("SELECT 1"))
        except SQLAlchemyError:
            return False
        return True
