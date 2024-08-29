"""
Functions for handling dates and times.

.. sourcecode:: ipython

    In [1]: import ffxiahbot.timeutils

The most useful functions are:
    * :py:func:`ffxiahbot.timeutils.timestamp`
    * :py:func:`ffxiahbot.timeutils.datetime`

.. sourcecode:: ipython

    In [2]: ffxiahbot.timeutils.timestamp('01/01/2015 00:00:00')
    Out[2]: 1420070400.0

    In [3]: ffxiahbot.timeutils.datetime('01/01/2015 00:00:00')
    Out[3]: datetime.datetime(2015, 1, 1)

.. seealso:: :py:mod:`datetime`, :py:class:`datetime.datetime`

Classes
-------

.. autosummary::
    :nosignatures:

    ffxiahbot.timeutils.DatetimeToTimestamp

Functions
---------

.. autosummary::
    :nosignatures:

    ffxiahbot.timeutils.str_to_datetime
    ffxiahbot.timeutils.datetime_to_str
    ffxiahbot.timeutils.datetime_to_timestamp
    ffxiahbot.timeutils.timestamp_to_datetime
    ffxiahbot.timeutils.datetime
    ffxiahbot.timeutils.timestamp

Documentation
-------------

.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""

import datetime as _datetime


def str_to_datetime(date_string):
    """
    Convert string to datetime object.

    :param date_string: string with format :code:`'%m/%d/%Y %H:%M:%S'`
    :type date_string: str

    :return: datetime object
    :rtype: :py:class:`datetime.datetime`

    .. sourcecode:: ipython

        In [1]: ffxiahbot.timeutils.str_to_datetime('01/01/2015 00:00:00')
        Out[1]: datetime.datetime(2015, 1, 1, 0, 0)

    .. seealso:: :py:meth:`datetime.datetime.strptime`
    """
    return _datetime.datetime.strptime(date_string, "%m/%d/%Y %H:%M:%S")


def datetime_to_str(datetime_obj):
    """
    Convert datetime object to string.

    :param datetime_obj: datetime object
    :type datetime_obj: :py:class:`datetime.datetime`

    :return: datetime as string
    :rtype: str

    .. sourcecode:: ipython

        In [1]: ffxiahbot.timeutils.datetime_to_str(datetime.datetime(2015, 1, 1))
        Out[1]: '01/01/2015 00:00:00'

    .. seealso:: :py:meth:`datetime.datetime.strftime`
    """
    return datetime_obj.strftime("%m/%d/%Y %H:%M:%S")


class DatetimeToTimestamp:
    """
    Convert datetime object to timestamp.

    Calculates the total seconds since 01/01/1970.

    .. warning:: Don't use this class directly.

    .. seealso:: :py:data:`ffxiahbot.timeutils.datetime_to_timestamp`
    """

    #: 01/01/1970
    epoch = _datetime.datetime(1970, 1, 1)

    def __call__(self, datetime_obj):
        return float((datetime_obj - self.epoch).total_seconds())


datetime_to_timestamp = DatetimeToTimestamp()
"""
Convert datetime object to timestamp.

:param datetime_obj: datetime object
:type datetime_obj: :py:class:`datetime.datetime`

:return: datetime as integer
:rtype: int

.. sourcecode:: ipython

    In [1]: ffxiahbot.timeutils.datetime_to_timestamp(datetime.datetime(2015, 1, 1, 0, 0))
    Out[1]: 1420070400.0

.. seealso:: :py:meth:`datetime.timedelta.total_seconds`
"""


def timestamp_to_datetime(stamp):
    """
    Convert timestamp to datetime object.

    :param stamp: seconds since epoch (01/01/1970)
    :type stamp: int, float

    :return: datetime object
    :rtype: :py:class:`datetime.datetime`

    .. sourcecode:: ipython

        In [1]: ffxiahbot.timeutils.timestamp_to_datetime(1420070400)
        Out[1]: datetime.datetime(2015, 1, 1, 0, 0)

    .. seealso:: :py:meth:`datetime.timedelta.utcfromtimestamp`
    """
    return _datetime.datetime.utcfromtimestamp(stamp)


def datetime(*args, **kwargs):
    """
    Convert anything (within reason) to a datetime object.

    When there are multiple arguments:
        * the :py:class:`datetime.datetime` constructor is called

    If there is only one argument:
        * if it is a :py:class:`datetime.datetime` it is returned
        * if it is a :py:obj:`str` it is passed to :py:func:`ffxiahbot.timeutils.str_to_datetime`
        * if it is a :py:obj:`int` it is passed to :py:func:`ffxiahbot.timeutils.timestamp_to_datetime`
        * if it is a :py:obj:`float` it is passed to :py:func:`ffxiahbot.timeutils.timestamp_to_datetime`

    :param args: positional arguments
    :param kwargs: keyword arguments

    .. sourcecode:: ipython

        In [1]: ffxiahbot.timeutils.datetime(datetime.datetime(2015, 1, 1))
        Out[1]: datetime.datetime(2015, 1, 1)

        In [2]: ffxiahbot.timeutils.datetime('01/01/2015 00:00:00')
        Out[2]: datetime.datetime(2015, 1, 1)

        In [3]: ffxiahbot.timeutils.datetime(1420070400.0)
        Out[3]: datetime.datetime(2015, 1, 1)

        In [4]: ffxiahbot.timeutils.datetime(1420070400)
        Out[4]: datetime.datetime(2015, 1, 1)

    .. seealso::

        :py:func:`ffxiahbot.timeutils.str_to_datetime`
        :py:func:`ffxiahbot.timeutils.timestamp_to_datetime`
        :py:class:`datetime.datetime`
    """
    if len(args) > 1 or kwargs:
        return _datetime.datetime(*args, **kwargs)

    try:
        obj = args[0]
    except IndexError:
        raise ValueError("expecting argument") from None

    if isinstance(obj, _datetime.datetime):
        return obj

    if isinstance(obj, str):
        return str_to_datetime(obj)

    if isinstance(obj, int):
        return timestamp_to_datetime(obj)

    if isinstance(obj, float):
        return timestamp_to_datetime(obj)

    raise TypeError(f"unknown type: {type(obj)}")


def timestamp(*args, **kwargs):
    """
    Convert anything (within reason) to a timestamp.

    :param args: positional arguments
    :param kwargs: keyword arguments

    * Passes arguments to :py:func:`ffxiahbot.timeutils.datetime`
    * Passes result to :py:data:`ffxiahbot.timeutils.datetime_to_timestamp`

    .. sourcecode:: ipython

        In [1]: ffxiahbot.timeutils.timestamp('01/01/2015 00:00:00')
        Out[1]: 1420070400.0

        In [2]: ffxiahbot.timeutils.timestamp(datetime.datetime(2015, 1, 1))
        Out[2]: 1420070400.0

        In [3]: ffxiahbot.timeutils.timestamp(1420070400.0)
        Out[3]: 1420070400.0

        In [4]: ffxiahbot.timeutils.timestamp(1420070400)
        Out[4]: 1420070400.0

    .. seealso::

        :py:func:`ffxiahbot.timeutils.datetime`
        :py:data:`ffxiahbot.timeutils.datetime_to_timestamp`
    """
    return datetime_to_timestamp(datetime(*args, **kwargs))


if __name__ == "__main__":
    pass
