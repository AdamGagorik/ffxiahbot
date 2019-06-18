from __future__ import absolute_import

__version__ = 0.1

from . import logutils
import logging

logutils.set_error()

try:
    import sqlalchemy
except ImportError as e:
    logging.exception(e.__class__.__name__)
    logging.error('pip install sqlalchemy')
    sqlalchemy = None
    exit(-1)

try:
    import pymysql
except ImportError as e:
    logging.exception(e.__class__.__name__)
    logging.error('pip install pymysql')
    pymysql = None
    exit(-1)

try:
    import bs4
except ImportError as e:
    logging.exception(e.__class__.__name__)
    logging.error('pip install beautifulsoup4')
    bs4 = None
    exit(-1)

try:
    import yaml
except ImportError as e:
    logging.exception(e.__class__.__name__)
    logging.error('pip install pyyaml')
    yaml = None
    exit(-1)

# noinspection PyPep8
from . import common
# noinspection PyPep8
from . import darkobject
# noinspection PyPep8
from . import database
# noinspection PyPep8
from . import item
# noinspection PyPep8
from . import itemlist
# noinspection PyPep8
from . import options
# noinspection PyPep8
from . import timeutils
