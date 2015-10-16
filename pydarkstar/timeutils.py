import datetime as _datetime


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


def timestamp(obj, *args, **kwargs):
    """
    Convert anything (within reason) to a timestamp.
    """
    return datetime_to_timestamp(datetime(obj, *args, **kwargs))


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


if __name__ == '__main__':
    pass
