"""
Alter item database.
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
import pydarkstar.itemlist
import pydarkstar.options
import pydarkstar.common

class Options(pydarkstar.options.Options):
    """
    Reads options from config file, then from command line.
    """
    def __init__(self):
        super(Options, self).__init__(config='alter.yaml', description=__doc__)

        # logging
        self.verbose   = False   # error, info, and debug
        self.silent    = False   # error only

        # input and output
        self.ifile     = None    # input file name
        self.ofile     = None    # output file name
        self.overwrite = False   # overwrite output
        self.backup    = False   # backup output
        self.save      = False   # save config

        # itemids
        self.all       = False   # all keys
        self.lambda_   = None    # ids that satisfy test
        self.match     = None    # names that match regex
        self.itemids   = []      # explicit list of ids

        # commands
        self.set       = []
        self.reset     = False
        self.create    = False
        self.scrub     = False
        self.execute   = False

        # logging
        self.add_argument('--verbose', action='store_true',
            help='report debug, info, and error')
        self.add_argument('--silent', action='store_true',
            help='report error only')

        # output
        self.add_argument(dest='ifile', nargs='?', type=str, default=self.ifile,
            help='output file stub')
        self.add_argument(dest='ofile', nargs='?', type=str, default=self.ofile,
            help='output file stub')
        self.add_argument('--overwrite', action='store_true',
            help='overwrite output file')
        self.add_argument('--backup', action='store_true',
            help='backup output file')
        self.add_argument('--save', action='store_true',
            help='save config file (and exit)')

        # itemids
        self.add_argument('--show', action='store_true',
            help='show itemids and exit')
        self.add_argument('--all', action='store_true',
            help='select all itemids')
        self.add_argument('--lambda', dest='lambda_', type=str, default=self.lambda_, metavar='lambda : True',
            help='select itemids where lambda evaluates to True')
        self.add_argument('--match', type=str, default=self.match, metavar='.*',
            help='select itemids where name matches regex')
        self.add_argument('--itemids', type=int, nargs='*', action='append', default=self.itemids, metavar='itemids',
            help='a list of item ids')

        # commands
        self.add_argument('--create', action='store_true',
            help='create a new item (if it doesnt exist)')
        self.add_argument('--reset', action='store_true',
            help='reset columns to defaults for item')
        self.add_argument('--scrub', action='store_true',
            help='redownload data for item')
        self.add_argument('--set', type=self.parse_tuple, metavar='key=value',
            help='set column to value for item')
        self.add_argument('--execute', action='store_true',
            help='actually run commands (default mode is a dry run)')

    def parse_args(self, args=None):
        super(Options, self).parse_args(args)

        itemids = []
        for obj in self.itemids:
            if isinstance(obj, list):
                itemids.extend(obj)
            else:
                itemids.append(obj)
        self.itemids = set(itemids)

        # check input and output names
        if self.ifile is None:
            # ifile=???, ofile=???
            if self.ofile is None:
                self.ofile = 'items.csv'
            # ifile=???, ofile=xxx
        else:
            # ifile=xxx, ofile=???
            if self.ofile is None:
                self.ofile = self.ifile
            # ifile=xxx, ofile=xxx

        if not self.overwrite and not self.backup:
            if os.path.exists(self.ofile):
                logging.error('output file already exists!\n\t%s', self.ofile)
                logging.error('please use --overwrite or --backup')
                exit(-1)

def main():
    """
    Main function.
    """
    # get options
    opts = Options()
    opts.parse_args()
    pydarkstar.logutils.basicConfig(
        verbose=opts.verbose, silent=opts.silent, fname='alter.log')
    logging.debug('start')

    # log options
    opts.log_values(level=logging.INFO)

    # save options
    if opts.save:
        opts.save = False
        opts.dump()
        return

    # load data
    ilist = pydarkstar.itemlist.ItemList()
    if opts.ifile:
        ilist.loadcsv(opts.ifile)
    ilist.info('loaded %d items', len(ilist))

    # select itemids
    if opts.all:
        opts.itemids = ilist.items.keys()
    else:
        tmp = opts.itemids
        opts.itemids = tmp

    # exit if there are no itemids
    if not opts.itemids:
        raise RuntimeError('no itemids passed or found!')

    # show itemids
    if opts.show:
        logging.info('%d itemids', len(opts.itemids))
        for i in opts.itemids:
            logging.info('exists=%d id=%d', i in ilist.items.keys(), i)
        exit(0)

    if not opts.create and not opts.reset and not opts.scrub and not opts.set:
        raise RuntimeError('nothing to do...')

    if opts.create:
        raise RuntimeError('not yet implemented')

    if opts.reset:
        raise RuntimeError('not yet implemented')

    if opts.scrub:
        raise RuntimeError('not yet implemented')

    if opts.set:
        raise RuntimeError('not yet implemented')

def cleanup():
    logging.info('exit\n')

if __name__ == '__main__':
    with pydarkstar.logutils.capture():
        main()
    cleanup()