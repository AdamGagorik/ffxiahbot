import datetime
import logging
import os
import re
import shutil


def create_path(*args, absolute=True, dt_fmt="%Y_%m_%d_%H_%M_%S", dt=None, **kwargs):
    """
    Construct a path.  You can access dt or datetime as objects.

    :param args: path components passed to :py:func:`os.path.join`
    :param absolute: make path absolute
    :param dt: datetime object
    :param dt_fmt: date format
    :param kwargs: variables passed to :py:func:`str.format`

    :type absolute: bool
    :type dt: :py:class:`datetime.datetime`
    :type dt_fmt: str
    """
    if not dt:
        dt = datetime.datetime.now()

    dt_str = dt.strftime(dt_fmt)
    _kwargs = {"dt": dt, "datetime": dt, "date": dt_str}
    _kwargs.update(**kwargs)

    path = os.path.expanduser(os.path.join(*args).format(**_kwargs))

    if absolute:
        return os.path.abspath(path)

    return path


def backup(path, copy=False):
    """
    Create backup file name.

    :param path: path of file
    :param copy: perform copy file
    """
    old_path = os.path.abspath(os.path.expanduser(path))

    # nothing to backup
    if not os.path.exists(old_path):
        return ""

    if not os.path.isfile(old_path):
        raise RuntimeError(f"can only backup files: {old_path}")

    # extract file info
    dname, bname = os.path.dirname(old_path), os.path.basename(old_path)
    root, dirs, files = next(os.walk(dname))

    # look for existing backups
    regex = re.compile(rf"^{bname}(\.(\d+))?$")
    found = []
    for f in files:
        match = regex.match(f)
        if match:
            try:
                found.append(int(match.group(2)))
            except TypeError:
                found.append(0)

    # should of at least found 1 if the file exists
    if not found:
        raise RuntimeError(f"can not backup file: {old_path}")

    # create backup name
    new_path = os.path.join(dname, f"{bname}.{max(found) + 1}")

    # validate old_path
    if os.path.exists(new_path) or new_path == old_path:
        raise RuntimeError(f"can not backup file: {old_path}")

    # copy the file
    if copy:
        logging.debug("backup (old): %s", old_path)
        logging.debug("backup (new): %s", new_path)
        shutil.copy(old_path, new_path)

    return new_path


def find_files(top, regex=r".*", r=False, ignorecase=True, **kwargs):
    """
    Search for files that match pattern.

    :param ignorecase: ignore case in regular expression
    :param top: top level directory
    :param regex: pattern to match
    :param r: recursive search
    """
    regex = re.compile(regex, re.IGNORECASE) if ignorecase else re.compile(regex)

    if r:
        for root, _dirs, files in os.walk(top, **kwargs):
            for f in files:
                match = regex.match(f)
                if match:
                    yield os.path.join(root, f)
    else:
        root, dirs, files = next(os.walk(top, **kwargs))
        for f in files:
            match = regex.match(f)
            if match:
                yield os.path.join(root, f)


if __name__ == "__main__":
    pass
