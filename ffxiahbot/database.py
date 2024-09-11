from __future__ import annotations

import contextlib
import logging
from collections.abc import Generator
from typing import Any

import sqlalchemy.exc
import sqlalchemy.orm
from sqlalchemy import URL


class Database:
    """
    Database connection using sqlalchemy.

    Args:
        url: sql database connection url
    """

    def __init__(self, url: str | URL, **kwargs: Any) -> None:
        super().__init__()

        # connect
        self.engine = sqlalchemy.create_engine(url, **kwargs)

        # create Session object
        self._Session = sqlalchemy.orm.sessionmaker(bind=self.engine)

    def session(self, **kwargs: Any) -> sqlalchemy.orm.Session:
        """
        Create session.
        """
        return self._Session(**kwargs)

    @contextlib.contextmanager
    def scoped_session(self, rollback: bool = True, fail: bool = False) -> Generator[sqlalchemy.orm.Session]:
        """
        Provide a transactional scope around a series of operations.

        Args:
            rollback: rollback transactions after catch
            fail: raise error after catch
        """
        session = self._Session()
        try:
            yield session

            # commit transactions
            session.commit()

        # catch errors
        except sqlalchemy.exc.SQLAlchemyError as e:
            # log the error
            logging.exception("caught SQL exception")

            # rollback transactions
            if rollback:
                session.rollback()

            # reraise error
            if fail:
                raise e from None

        # cleanup
        finally:
            session.close()

    @classmethod
    def sqlite(cls, database: str = ":memory:", **kwargs: Any) -> Database:
        """
        Alternate constructor.  dialect=sqlite (in-memory)
        """
        url = URL.create("sqlite", database=database)
        return cls(url, **kwargs)

    @classmethod
    def pymysql(cls, hostname: str, database: str, username: str, password: str, port: int, **kwargs: Any) -> Database:
        """
        Alternate constructor.  dialect=mysql, driver=pymysql

        Args:
            hostname: database hostname
            database: database name
            username: database username
            password: database password
            port: database port
        """
        url = URL.create(
            "mysql+pymysql",
            username=username,
            password=password,  # plain (unescaped) text
            host=hostname,
            database=database,
            port=port,
        )
        return cls(url, **kwargs)

    def __str__(self) -> str:
        return repr(self.engine)
