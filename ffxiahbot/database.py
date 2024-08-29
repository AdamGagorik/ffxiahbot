import contextlib
import logging

import sqlalchemy.exc
import sqlalchemy.orm

from ffxiahbot.darkobject import DarkObject


class Database(DarkObject):
    """
    Database connection using sqlalchemy.

    :param url: sql database connection url
    """

    def __init__(self, url, **kwargs):
        super().__init__()

        # connect
        self.engine = sqlalchemy.create_engine(url, **kwargs)

        # create Session object
        self._Session = sqlalchemy.orm.sessionmaker(bind=self.engine)

    def session(self, **kwargs):
        """
        Create session.
        """
        return self._Session(**kwargs)

    @contextlib.contextmanager
    def scoped_session(self, rollback=True, fail=False):
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
        except sqlalchemy.exc.SQLAlchemyError:
            # log the error
            logging.exception("caught SQL exception")

            # rollback transactions
            if rollback:
                session.rollback()

            # reraise error
            if fail:
                raise RuntimeError("SQL Failed") from None

        # cleanup
        finally:
            session.close()

    @classmethod
    def pymysql(cls, hostname, database, username, password):
        """
        Alternate constructor.  dialect=mysql, driver=pymysql

        :param hostname: database connection parameter
        :param database: database connection parameter
        :param username: database connection parameter
        :param password: database connection parameter
        """
        url = cls.format_url("mysql", "pymysql", hostname, database, username, password)
        obj = cls(url)
        return obj

    @staticmethod
    def format_url(dialect, driver, hostname, database, username, password):
        """
        Create connection url.
        """
        return "{}://{u}:{p}@{h}/{d}".format(
            "+".join([dialect, driver]), h=hostname, d=database, u=username, p=password
        )

    def __str__(self):
        return repr(self.engine)
