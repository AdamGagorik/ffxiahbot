# -*- coding: utf-8 -*-
"""
Create item database.
"""
import logging
import os
import re

from .options import Options

from ... import common
from ... import logutils
from ...scrubbing import ffxiah
from ...itemlist import ItemList


def main():
    """
    Main function.
    """
    # get options
    opts = Options()

    # check output file name validity
    oname = os.path.abspath('{}.csv'.format(re.sub(r'\.csv$', '', opts.stub)))
    if not opts.overwrite and not opts.backup:
        if os.path.exists(oname):
            logging.error('output file already exists!\n\t%s', oname)
            logging.error('please use --overwrite or --backup')
            exit(-1)

    # scub data
    scrubber = ffxiah.FFXIAHScrubber()
    scrubber.save = False
    data = scrubber.scrub(force=True, threads=-1, urls=opts.urls, ids=opts.itemids)

    # create item list from data
    ilist = ItemList()
    for itemid in data:
        kwargs = ffxiah.extract(data, itemid, stock01=opts.stock01, stock12=opts.stock12)
        ilist.add(itemid, **kwargs)

    # backup file
    if opts.backup:
        common.backup(oname, copy=True)

    # overwrites if exists, but we checked already
    ilist.savecsv(oname)


def cleanup():
    logging.info('exit\n')


if __name__ == '__main__':
    with logutils.capture():
        main()
    cleanup()
