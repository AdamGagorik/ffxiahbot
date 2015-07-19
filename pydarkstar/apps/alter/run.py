# -*- coding: utf-8 -*-
"""
Alter item database.
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
    logutils.basic_config(verbose=opts.verbose, silent=opts.silent, fname='pydarkstar.log')
    opts.log_values(level=logging.INFO)

    # check output file name validity
    oname = os.path.abspath('{}.csv'.format(re.sub(r'\.csv$', '', opts.stub)))
    if not opts.overwrite and not opts.backup:
        if os.path.exists(oname):
            logging.error('output file already exists!\n\t%s', oname)
            logging.error('please use --overwrite or --backup')
            exit(-1)

    # load data
    idata = ItemList.from_csv(*opts.data)

    # collect itemids
    itemids = set()

    # from items
    if opts.all:
        logging.info('select: --all')
        itemids.update(idata.items.keys())

    # filter itemids
    if opts.lambda_:
        logging.info('select: lambda x : %s', opts.lambda_)
        func = eval('lambda x : {}'.format(opts.lambda_))
        itemids.update([i for i in idata.items.keys() if func(i)])

    # filter names
    if opts.match:
        logging.info('select: name %s', opts.match)
        regex = re.compile(opts.match, re.IGNORECASE)
        itemids.update([i for i in idata.items.keys() if regex.match(idata[i].name)])

    # passed
    if opts.itemids:
        logging.info('select: %d itemids passed', len(opts.itemids))
        itemids.update(opts.itemids)

    logging.info('%d items selected', len(itemids))

    # validate
    if not itemids.issubset(idata.items.keys()):
        raise RuntimeError('invalid itemids')

    # exit if there are no itemids
    if not itemids:
        raise RuntimeError('no itemids passed or found!')

    # check action validity
    if not any([opts.show, opts.scrub, opts.set]):
        raise RuntimeError('nothing to do! use --show --reset --scrub or --set')

    # show itemids
    if opts.show:
        logging.info('%d itemids', len(itemids))
        for i in itemids:
            logging.info(str(idata[i]))
        exit(0)

    # rescrub data
    if opts.scrub:
        scrubber = ffxiah.FFXIAHScrubber()
        scrubber.save = False
        data = scrubber.scrub(force=True, threads=-1, urls=None, ids=itemids)
        for i in data:
            logging.debug('Item(%06d) updated', i)
            idata.set(i, **ffxiah.extract(data, i))

    # set values
    if opts.set:
        logging.info('--set %s=%s', *opts.set)
        for i in itemids:
            if hasattr(idata[i], opts.set[0]):
                setattr(idata[i], opts.set[0], opts.set[1])
                logging.debug('Item(%06d) %s=%s', i, opts.set[0], getattr(idata[i], opts.set[0]))
            else:
                raise RuntimeError('Item does not have attribute %s', opts.set[0])

    # backup file
    if opts.backup:
        common.backup(oname, copy=True)

    # overwrites if exists, but we checked already
    idata.savecsv(oname)


def cleanup():
    logging.info('exit\n')


if __name__ == '__main__':
    with logutils.capture():
        main()
    cleanup()
