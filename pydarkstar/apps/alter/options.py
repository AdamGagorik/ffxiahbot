# -*- coding: utf-8 -*-
"""
Alter item database.
"""
from ... import options
import os


class Options(options.Options):
    """
    Reads options from config file, then from command line.
    """

    def __init__(self):
        super(Options, self).__init__(config='alter.yaml', description=__doc__)

        # logging
        self.verbose = False  # error, info, and debug
        self.silent = False  # error only

        # input and output
        self.ifile = 'items.csv'  # input file name
        self.ofile = None  # output file name
        self.overwrite = False  # overwrite output
        self.backup = False  # backup output
        self.save = False  # save config

        # itemids
        self.all = False  # all keys
        self.lambda_ = None  # ids that satisfy test
        self.match = None  # names that match regex
        self.itemids = []  # explicit list of ids

        # commands
        self.show = False
        self.scrub = False
        self.set = []

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
        group.add_argument('--scrub', action='store_true',
                           help='redownload data for item')
        group.add_argument('--set', type=self.parse_tuple, metavar='key=value',
                           help='set column to value for item')

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
            self.ifile = os.path.abspath(os.path.expanduser(self.ifile))
            # ifile=xxx, ofile=???
            if self.ofile is None:
                self.ofile = self.ifile
                # ifile=xxx, ofile=xxx
        self.ofile = os.path.abspath(os.path.expanduser(self.ofile))


if __name__ == '__main__':
    pass
