# -*- coding: utf-8 -*-
"""
Refill the auction house.
"""
import logging

from .options import Options

from ... import logutils
from ...itemlist import ItemList
from ...database import Database
from ...auction.manager import Manager


def main():
    """
    Main function.
    """
    # get options
    opts = Options()
    logutils.basic_config(verbose=opts.verbose, silent=opts.silent, fname='pydarkstar.log')
    opts.log_values(level=logging.INFO)

    # create auction house manager
    manager = Manager.create_database_and_manager(
        hostname=opts.hostname,
        database=opts.database,
        username=opts.username,
        password=opts.password,
        name=opts.name,
        fail=opts.fail
    )

    # make sure there is data
    if not opts.data:
        raise RuntimeError('missing item data CSV!')

    # load data
    logging.info('loading item data...')
    idata = ItemList()
    for f in opts.data:
        idata.loadcsv(f)

    if not opts.force:
        raise RuntimeError('refilling all items from auction house is dangerous. use --force')
    else:
        logging.info('restocking...')
        manager.restock_items(itemdata=idata)
        logging.info('exit after restock')
        return


def cleanup():
    logging.info('exit\n')


if __name__ == '__main__':
    with logutils.capture():
        main()
    cleanup()
