import datetime as _datetime
import random as _random


def randomdt(month=None, day=None, year=None, hour=None, minute=None, second=None,
             microsecond=None, tzinfo=None, month_range=(1, 12), day_range=(1, 31),
             year_range=(1900, 2000), hour_range=(0, 23), minute_range=(0, 59),
             second_range=(0, 59), microsecond_range=(0, 0)):
    """
    Create a random datetime object.

    :param month: month
    :param day: day
    :param year: year
    :param hour: hour
    :param minute: minute
    :param second: second
    :param microsecond: microsecond
    :param tzinfo: time zone info
    :param month_range: (min, max) month
    :param day_range: (min, max) day
    :param year_range: (min, max) year
    :param hour_range: (min, max) hour
    :param minute_range: (min, max) minute
    :param second_range: (min, max) second
    :param microsecond_range: (min, max) microsecond
    :return: datetime
    :rtype: py:class:`datetime.datetime`

    .. seealso:: py:class:`datetime.datetime`
    """
    if month is None:
        month = _random.randint(*month_range)

    if day is None:
        day = _random.randint(*day_range)

    if year is None:
        year = _random.randint(*year_range)

    if hour is None:
        hour = _random.randint(*hour_range)

    if minute is None:
        minute = _random.randint(*minute_range)

    if second is None:
        second = _random.randint(*second_range)

    if microsecond is None:
        microsecond = _random.randint(*microsecond_range)

    for i in range(3):
        try:
            return _datetime.datetime(year, month, day - i, hour, minute, second, microsecond, tzinfo)
        except ValueError:
            pass

    return _datetime.datetime(year, month, day - 3, hour, minute, second, microsecond)


def str_to_datetime(date_string):
    """
    Convert string to datetime object.
    """
    return _datetime.datetime.strptime(date_string, '%m/%d/%Y %H:%M:%S')


def datetime_to_str(datetime_obj):
    """
    Convert datetime object to string.
    """
    return '{dt.month:>02}/{dt.day:>02}/{dt.year} {dt.hour:>02}:{dt.minute:>02}:{dt.second:>02}'.format(dt=datetime_obj)


class DatetimeToTimestamp(object):
    """
    Convert datetime object to timestamp.
    """
    epoch = _datetime.datetime(1970, 1, 1)

    def __call__(self, datetime_obj):
        return float((datetime_obj - self.epoch).total_seconds())


datetime_to_timestamp = DatetimeToTimestamp()


def timestamp_to_datetime(stamp):
    """
    Convert timestamp to datetime object.
    """
    return _datetime.datetime.utcfromtimestamp(stamp)


def datetime(*args, **kwargs):
    """
    Convert anything (within reason) to a datetime object.
    """
    if len(args) > 1 or kwargs:
        return _datetime.datetime(*args, **kwargs)

    try:
        obj = args[0]
    except IndexError:
        raise ValueError('expecting argument')

    if isinstance(obj, _datetime.datetime):
        return obj

    if isinstance(obj, str):
        return str_to_datetime(obj)

    if isinstance(obj, int):
        return timestamp_to_datetime(obj)

    if isinstance(obj, float):
        return timestamp_to_datetime(obj)

    raise TypeError('unknown type: %s' % type(obj))


def timestamp(obj, *args, **kwargs):
    """
    Convert anything (within reason) to a timestamp.
    """
    return datetime_to_timestamp(datetime(obj, *args, **kwargs))


if __name__ == '__main__':
    pass
