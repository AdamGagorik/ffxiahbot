from __future__ import annotations

import contextlib
import logging
from typing import Any

import sqlalchemy.exc
import sqlalchemy.orm


class Database:
    """
    Database connection using sqlalchemy.

    :param url: sql database connection url
    """

    def __init__(self, url: str, **kwargs):
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
    def scoped_session(self, rollback: bool = True, fail: bool = False) -> sqlalchemy.orm.Session:
        """
        Provide a transactional scope around a series of operations.

        :param rollback: rollback transactions after catch
        :param fail: raise error after catch

        :type rollback: bool
        :type fail: bool
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
    def pymysql(cls, hostname: str, database: str, username: str, password: str, port: int) -> Database:
        """
        Alternate constructor.  dialect=mysql, driver=pymysql

        Args:
            hostname: database hostname
            database: database name
            username: database username
            password: database password
            port: database port
        """
        url = cls.format_url("mysql", "pymysql", hostname, database, username, password, port)
        obj = cls(url)
        return obj

    @staticmethod
    def format_url(
        dialect: str, driver: str, hostname: str, database: str, username: str, password: str, port: int
    ) -> str:
        """
        Create connection url.
        """
        return "{}://{username}:{password}@{hostname}:{port}/{database}".format(
            "+".join([dialect, driver]),
            hostname=hostname,
            database=database,
            username=username,
            password=password,
            port=port,
        )

    def __str__(self) -> str:
        return repr(self.engine)
