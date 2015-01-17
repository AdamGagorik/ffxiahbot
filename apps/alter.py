"""
Alter item database.
"""
import logging
import os
import re

import pydarkstar.scrubbing.ffxiah
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
        self.show      = False
        self.reset     = False
        self.scrub     = False
        self.set       = []

        # run
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

        # itemids selection
        group = self.add_mutually_exclusive_group()
        group.add_argument('--all', action='store_true',
            help='select all itemids')
        group.add_argument('--lambda', dest='lambda_', type=str, default=self.lambda_, metavar='lambda : True',
            help='select itemids where lambda evaluates to True')
        group.add_argument('--match', type=str, default=self.match, metavar='.*',
            help='select itemids where name matches regex')
        group.add_argument('--itemids', type=int, nargs='*', action='append', default=self.itemids, metavar='itemids',
            help='a list of item ids')

        # commands
        group = self.add_mutually_exclusive_group()
        group.add_argument('--show', action='store_true',
            help='show itemids and exit')
        group.add_argument('--reset', action='store_true',
            help='reset columns to defaults for item')
        group.add_argument('--scrub', action='store_true',
            help='redownload data for item')
        group.add_argument('--set', type=self.parse_tuple, metavar='key=value',
            help='set column to value for item')

        # run
        self.add_argument('--execute', action='store_true',
            help='actually run commands (default mode is a dry run)')

    def parse_args(self, args=None):
        super(Options, self).parse_args(args)

        if not self.show and not self.reset and not self.scrub and not self.set:
            raise RuntimeError('nothing to do! use --show --reset --scrub or --set')

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

        # check output file
        if not self.overwrite and not self.backup:
            if os.path.exists(self.ofile):
                logging.error('output file already exists!\n\t%s', self.ofile)
                logging.error('please use --overwrite or --backup')
                exit(-1)

def main(args=None):
    """
    Main function.
    """
    # get options
    opts = Options()
    opts.parse_args(args)
    pydarkstar.logutils.basicConfig(
        verbose=opts.verbose, silent=opts.silent, fname='alter.log')
    logging.info('start')

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

    # collect itemids
    itemids = set()

    # from items
    if opts.all:
        logging.info('select: --all')
        itemids.update(ilist.items.keys())

    # filter itemids
    if opts.lambda_:
        logging.info('select: lambda x : %s', opts.lambda_)
        func = eval('lambda x : {}'.format(opts.lambda_))
        itemids.update([i for i in ilist.items.keys() if func(i)])

    # filter names
    if opts.match:
        logging.info('select: name %s', opts.match)
        regex = re.compile(opts.match, re.IGNORECASE)
        itemids.update([i for i in ilist.items.keys() if regex.match(ilist[i].name)])

    # passed
    if opts.itemids:
        logging.info('select: %d itemids passed', len(opts.itemids))
        itemids.update(opts.itemids)

    logging.info('%d items selected', len(itemids))

    # validate
    if not itemids.issubset(ilist.items.keys()):
        raise RuntimeError('invalid itemids')

    # exit if there are no itemids
    if not itemids:
        raise RuntimeError('no itemids passed or found!')

    # show itemids
    if opts.show:
        logging.info('%d itemids', len(itemids))
        for i in itemids:
            logging.info(str(ilist[i]))
        exit(0)

    # reset to defaults
    if opts.reset:
        raise RuntimeError('not yet implemented')

    # rescrub data
    if opts.scrub:
        scrubber = pydarkstar.scrubbing.ffxiah.FFXIAHScrubber()
        scrubber.save = False
        data = scrubber.scrub(force=True, threads=-1, urls=None, ids=itemids)
        for i in data:
            logging.debug('Item(%06d) updated', i)
            ilist.set(i, **pydarkstar.scrubbing.ffxiah.extract(data, i))

    # set values
    if opts.set:
        logging.info('--set %s=%s', *opts.set)
        for i in itemids:
            if hasattr(ilist[i], opts.set[0]):
                setattr(ilist[i], opts.set[0], opts.set[1])
                logging.debug('Item(%06d) %s=%s', i, opts.set[0], getattr(ilist[i], opts.set[0]))
            else:
                raise RuntimeError('Item does not have attribute %s', opts.set[0])

def cleanup():
    logging.info('exit\n')

if __name__ == '__main__':
    with pydarkstar.logutils.capture():
        main()
    cleanup()