"""
Buy and sell items on the auction house.
"""
import datetime
import logging
import time
import sys
import os

# import hack to avoid PYTHONPATH
try:
    import pydarkstar
except ImportError:
    root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    root, dirs, files = next(os.walk(root))
    if 'pydarkstar' in dirs:
        sys.path.insert(1, root)
        import pydarkstar
    else:
        raise

import pydarkstar.logutils
import pydarkstar.itemlist
import pydarkstar.options
import pydarkstar.common

import pydarkstar.database
import pydarkstar.auction.manager

class Options(pydarkstar.options.Options):
    """
    Reads options from config file, then from command line.
    """
    def __init__(self):
        super(Options, self).__init__(config='broker.yaml', description=__doc__)

        # logging
        self.verbose  = False # error, info, and debug
        self.silent   = False # error only

        # input
        self.data     = []    # list of itemdata
        self.find     = False # search for item data

        # output
        self.save     = False # save config

        # sql
        self.hostname = '127.0.0.1'
        self.database = 'dspdb'
        self.username = 'root'
        self.password = ''
        self.fail     = False # fail on SQL errors

        # cleaning
        self.clear    = False # clear items sold by broker
        self.all      = False # clear all items
        self.force    = False # clear all items check

        # selling
        self.name     = 'Zissou' # seller name
        self.restock  = 3600     # restock tick
        self.refill   = False    # restock at start

        # buying
        self.tick     = 30    # buying interval

        # logging
        self.add_argument('--verbose', action='store_true',
            help='report debug, info, and error')
        self.add_argument('--silent', action='store_true',
            help='report error only')

        # input
        self.add_argument(dest='data', nargs='*', type=str, default=self.data,
            metavar='str', help='item data CSV file(s)')
        self.add_argument('--find', action='store_true',
            help='search for item data files')

        # output
        self.add_argument('--save', action='store_true',
            help='save config file (and exit)')

        # sql
        self.add_argument('--hostname', default=self.hostname, type=str,
            metavar='str', help='SQL address')
        self.add_argument('--database', default=self.database, type=str,
            metavar='str', help='SQL database')
        self.add_argument('--username', default=self.username, type=str,
            metavar='str', help='SQL username')
        self.add_argument('--password', default=self.password, type=str,
            metavar='str', help='SQL password')
        self.exclude('password')
        self.add_argument('--fail', action='store_true',
            help='fail on SQL errors')

        # cleaning
        self.add_argument('--clear', action='store_true',
            help='clear items sold by seller')
        self.add_argument('--all', action='store_true',
            help='clear *all* items')
        self.add_argument('--force', action='store_true',
            help='clear *all* items')

        # selling
        self.add_argument('--name', type=str, default=self.name,
            metavar='str', help='seller name')
        self.add_argument('--restock', type=int, default=self.restock,
            metavar='int', help='restock interval in seconds')
        self.add_argument('--refill', action='store_true',
            help='restock items at start and exit')

        # buying
        self.add_argument('--tick', type=int, default=self.tick,
            metavar='int', help='buying interval in seconds')

    def parse_args(self, args=None):
        super(Options, self).parse_args(args)
        self.data = set(self.data)

        # find data files
        if self.find:
            found = list(pydarkstar.common.findFiles(
                top=os.getcwd(), regex=r'.*\.csv', r=False, ignorecase=True))
            self.data.update(found)

        self.data = list(self.data)

def main():
    """
    Main function.
    """
    # get options
    opts = Options()
    opts.parse_args()
    pydarkstar.logutils.basicConfig(
        verbose=opts.verbose, silent=opts.silent, fname='broker.log')
    logging.debug('start')

    # log options
    opts.log_values(level=logging.INFO)

    # save options
    if opts.save:
        opts.save = False
        opts.dump()
        return

    # connect to database
    db = pydarkstar.database.Database.pymysql(
        hostname=opts.hostname,
        database=opts.database,
        username=opts.username,
        password=opts.password,
    )

    # create auction house manager
    manager = pydarkstar.auction.manager.Manager(db, fail=opts.fail)
    manager.seller.seller_name = opts.name
    manager.buyer.buyer_name   = opts.name

    if opts.clear:
        # clear all items
        if opts.all:
            # really?
            if not opts.force:
                raise RuntimeError('clearing all items from auction house is dangerous. use --force')
            else:
                manager.cleaner.clear(seller=None)
        # clear seller items
        else:
            manager.cleaner.clear(seller=manager.seller.seller)

        # exit after clearing
        logging.info('exit after clear')
        return

    # make sure there is data
    if not opts.data:
        raise RuntimeError('missing item data CSV!')

    # load data
    idata = pydarkstar.itemlist.ItemList()
    for f in opts.data:
        idata.loadcsv(f)

    if opts.refill:
        manager.restockItems(itemdata=idata)
        logging.info('exit after restock')
        return

    logging.info('starting main loop')
    start = datetime.datetime.now()
    last  = start
    while True:
        now = datetime.datetime.now()
        delta = (now - last).total_seconds()
        elapsed = (now - start).total_seconds()
        logging.info('time=%012.1f s last restock=%012.1f s next restock=%012.1f s',
            elapsed, delta, opts.restock - delta)

        if delta >= opts.restock:
            manager.restockItems(itemdata=idata)
            last = datetime.datetime.now()

        # buy items
        manager.buyItems(itemdata=idata)

        # sleep until next tick
        logging.info('wait=%012.1f s', opts.tick)
        time.sleep(opts.tick)

def cleanup():
    logging.info('exit\n')

if __name__ == '__main__':
    with pydarkstar.logutils.capture():
        main()
    cleanup()
