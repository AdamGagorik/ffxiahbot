# -*- coding: utf-8 -*-
"""
Buy and sell items on the auction house.
"""
import datetime
import logging
import time

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
    opts.parse_args()
    logutils.basic_config(verbose=opts.verbose, silent=opts.silent, fname='pydarkstar.log')
    logging.info('start')

    # log options
    opts.log_values(level=logging.INFO)

    # connect to database
    db = Database.pymysql(
        hostname=opts.hostname,
        database=opts.database,
        username=opts.username,
        password=opts.password,
    )

    # create auction house manager
    manager = Manager(db, fail=opts.fail)
    manager.seller.seller_name = opts.name
    manager.buyer.buyer_name = opts.name

    # make sure there is data
    if not opts.data:
        raise RuntimeError('missing item data CSV!')

    # load data
    logging.info('loading item data...')
    idata = ItemList()
    for f in opts.data:
        idata.loadcsv(f)

    if opts.refill:
        logging.info('restocking...')
        manager.restock_items(itemdata=idata)
        logging.info('exit after restock')
        return

    logging.info('starting main loop...')
    start = datetime.datetime.now()
    last = start
    while True:
        now = datetime.datetime.now()
        delta = (now - last).total_seconds()
        elapsed = (now - start).total_seconds()
        logging.debug('time=%012.1f s last restock=%012.1f s next restock=%012.1f s',
                      elapsed, delta, opts.restock - delta)

        if delta >= opts.restock:
            logging.debug('restocking...')
            manager.restock_items(itemdata=idata)
            last = datetime.datetime.now()

        # buy items
        manager.buy_items(itemdata=idata)

        # sleep until next tick
        logging.debug('wait=%012.1f s', opts.tick)
        time.sleep(opts.tick)


def cleanup():
    logging.info('exit\n')


if __name__ == '__main__':
    with logutils.capture():
        main()
    cleanup()
