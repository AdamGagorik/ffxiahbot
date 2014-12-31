"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import logging
import shutil
import os
import re

def backup(path, copy=False):
    """
    Create backup file name.

    :param path: path of file
    :param copy: perform copy file
    """
    old_path = os.path.abspath(os.path.expanduser(path))

    # nothing to backup
    if not os.path.exists(old_path):
        return ''

    if not os.path.isfile(old_path):
        raise RuntimeError('can only backup files: %s' % old_path)

    # extract file info
    dname, bname = os.path.dirname(old_path), os.path.basename(old_path)
    root, dirs, files = next(os.walk(dname))

    # look for existing backups
    regex = re.compile('^{}(\.(\d+))?$'.format(bname))
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
        raise RuntimeError('can not backup file: %s' % old_path)

    # create backup name
    new_path = os.path.join(dname, '{}.{}'.format(bname, max(found) + 1))

    # validate old_path
    if os.path.exists(new_path) or new_path == old_path:
        raise RuntimeError('can not backup file: %s' % old_path)

    # copy the file
    if not copy:
        logging.debug('backup (old): %s', old_path)
        logging.debug('backup (new): %s', new_path)
        shutil.copy(old_path, new_path)

    return new_path

if __name__ == '__main__':
    pass