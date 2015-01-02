"""
Create item database.
"""
import logging
import sys
import os
import re

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
import pydarkstar.scrub.ffxiah
import pydarkstar.itemlist
import pydarkstar.options
import pydarkstar.common

class Options(pydarkstar.options.Options):
    """
    Reads options from config file, then from command line.
    """
    def __init__(self):
        super(Options, self).__init__(config='scrub.yaml', description=__doc__)
        self.verbose   =  False   # error, info, and debug
        self.silent    =  False   # error only
        self.stub      =  'items' # output file stub
        self.overwrite =  False   # overwrite output
        self.backup    =  False   # backup output
        self.save      =  False   # save config
        self.force     =  False   # redownload
        self.threads   = -1       # cpu threads during download
        self.stock01   =  5       # default stock for singles
        self.stock12   =  5       # default stock for stacks
        self.itemids   = []       # a list of item ids
        self.urls      = []       # a list of category urls

        # logging
        self.add_argument('--verbose', action='store_true',
            help='report debug, info, and error')
        self.add_argument('--silent', action='store_true',
            help='report error only')

        # output
        self.add_argument(dest='stub', nargs='?', type=str, default=self.stub,
            help='output file stub')
        self.add_argument('--overwrite', action='store_true',
            help='overwrite output file')
        self.add_argument('--backup', action='store_true',
            help='backup output file')
        self.add_argument('--save', action='store_true',
            help='save config file (and exit)')

        # scrubbing parameters
        self.add_argument('--force', action='store_true',
            help='start from scratch')
        self.add_argument('--threads', type=int, default=self.threads, metavar=self.threads,
            help='number of cpu threads to use')
        self.add_argument('--urls', type=str, nargs='*', action='append', default=self.urls, metavar='url',
            help='a list of category urls')
        self.add_argument('--itemids', type=str, nargs='*', action='append', default=self.itemids, metavar='itemids',
            help='a list of item ids')

        # defaults
        self.add_argument('--stock01', type=int, default=self.stock01, metavar=self.stock01,
            help='default stock for singles')
        self.add_argument('--stock12', type=int, default=self.stock12, metavar=self.stock12,
            help='default stock for stacks')

        self.exclude('itemids')
        self.exclude('urls')

    def parse_args(self, args=None):
        super(Options, self).parse_args(args)

        urls = []
        for obj in self.urls:
            if isinstance(obj, list):
                urls.extend(obj)
            else:
                urls.append(obj)
        self.urls = urls

        itemids = []
        for obj in self.itemids:
            if isinstance(obj, list):
                itemids.extend(obj)
            else:
                itemids.append(obj)
        self.itemids = itemids

def main():
    """
    Main function.
    """
    # get options
    opts = Options()
    opts.parse_args()
    pydarkstar.logutils.basicConfig(
        verbose=opts.verbose, silent=opts.silent, fname='scrub.log')
    logging.debug('start')

    # log options
    opts.log_values(level=logging.INFO)

    # save options
    if opts.save:
        opts.save = False
        opts.dump()
        return

    # check output file name validity
    oname = os.path.abspath('{}.csv'.format(re.sub(r'\.csv$', '', opts.stub)))
    if not opts.overwrite and not opts.backup:
        if os.path.exists(oname):
            logging.error('output file already exists!\n\t%s', oname)
            logging.error('please use --overwrite or --backup')
            exit(-1)

    # scrub data
    scrubber = pydarkstar.scrub.ffxiah.FFXIAHScrubber()
    data = scrubber.scrub(force=opts.force, threads=opts.threads, urls=opts.urls, ids=opts.itemids)

    # create item list from data
    ilist = pydarkstar.itemlist.ItemList()
    for itemid in data:

        # singles
        try:
            price01, sell01 = data[itemid]['median'], True

            # do not sell items without a price
            if price01 <= 0:
                price01, sell01 = None, False

        except KeyError:
            price01, sell01 = None, False

        # stacks
        try:
            price12, sell12 = data[itemid]['stack price'], True

            # do not sell items without a price
            if price12 <= 0:
                price12, sell12 = None, False

        except KeyError:
            price12, sell12 = None, False

        # the name doesn't really matter
        try:
            name = data[itemid]['name']
        except KeyError:
            name=None

        ilist.add(itemid, name=name,
            price01=price01, stock01=opts.stock01, sell01=sell01, buy01=True,
            price12=price12, stock12=opts.stock12, sell12=sell12, buy12=True)

    # backup file
    if opts.backup:
        pydarkstar.common.backup(oname)

    # overwrites if exists, but we checked already
    ilist.savecsv(oname)

def cleanup():
    logging.info('exit\n')

if __name__ == '__main__':
    with pydarkstar.logutils.capture():
        main()
    cleanup()
