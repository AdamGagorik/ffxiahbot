# -*- coding: utf-8 -*-
"""
Alter item database.
"""
from ...options.basic import BasicOptions
from ...options.input import InputOptions
from ...options.output import OutputOptions


class Options(OutputOptions, InputOptions, BasicOptions):
    """
    Reads options from config file, then from command line.
    """

    def __init__(self):
        super(Options, self).__init__(description=__doc__)

        # itemids selection
        self.all = False  # all keys
        self.lambda_ = None  # ids that satisfy test
        self.match = None  # names that match regex
        self.itemids = []  # explicit list of ids

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
        self.show = False
        self.scrub = False
        self.set = []

        group = self.add_mutually_exclusive_group()
        group.add_argument('--show', action='store_true',
                           help='show itemids and exit')
        group.add_argument('--scrub', action='store_true',
                           help='redownload data for item')
        group.add_argument('--set', type=self.parse_tuple, metavar='key=value',
                           help='set column to value for item')

    def __after__(self):
        super(Options, self).__after__()

        itemids = []
        for obj in self.itemids:
            if isinstance(obj, list):
                itemids.extend(obj)
            else:
                itemids.append(obj)
        self.itemids = set(itemids)


if __name__ == '__main__':
    pass
