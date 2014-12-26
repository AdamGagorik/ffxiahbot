"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.exc
import pydarkstar.darkobject
import contextlib
import logging

class Database(pydarkstar.darkobject.DarkObject):
    """
    Database connection using sqlalchemy.

    :param url: sql database connection url
    """
    def __init__(self, url, **kwargs):
        super(Database, self).__init__()

        # connect
        self.engine = sqlalchemy.create_engine(url, **kwargs)

        # create Session object
        self._Session = sqlalchemy.orm.sessionmaker(bind=self.engine)

    def session(self, *args, **kwargs):
        """
        Create session.
        """
        return self._Session(*args, **kwargs)

    @contextlib.contextmanager
    def scoped_session(self, reraise=False, rollback=True):
        """
        Provide a transactional scope around a series of operations.

        :param reraise: raise error after catch
        :param rollback: rollback transactions after catch

        :type reraise: bool
        :type rollback: bool
        """
        session = self._Session()
        try:
            yield session

            # commit transactions
            session.commit()

        # catch errors
        except sqlalchemy.exc.SQLAlchemyError:
            # log the error
            logging.exception('caught SQL exception')

            # rollback transactions
            if rollback:
                session.rollback()

            # reraise error
            if reraise:
                raise

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
        url = cls.format_url('mysql', 'pymysql', hostname, database, username, password)
        obj = cls(url)
        return obj

    @staticmethod
    def format_url(dialect, driver, hostname, database, username, password):
        """
        Create connection url.
        """
        return '{}://{u}:{p}@{h}/{d}'.format('+'.join([dialect, driver]),
            h=hostname, d=database, u=username, p=password)

    def __str__(self):
        return repr(self.engine)