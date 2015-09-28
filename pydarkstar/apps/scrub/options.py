# -*- coding: utf-8 -*-
"""
Create item database.
"""
from ...options.basic import BasicOptions
from ...options.output import OutputOptions


class Options(OutputOptions, BasicOptions):
    """
    Reads options from config file, then from command line.
    """

    def __init__(self):
        super(Options, self).__init__(description=__doc__)
        self.stock01 = 5  # default stock for singles
        self.stock12 = 5  # default stock for stacks
        self.itemids = []  # a list of item ids
        self.urls = []  # a list of category urls

        self.add_argument('--urls', type=str, nargs='*', action='append', default=self.urls, metavar='url',
                          help='a list of category urls')
        self.add_argument('--itemids', type=int, nargs='*', action='append', default=self.itemids, metavar='itemids',
                          help='a list of item ids')
        self.add_argument('--stock01', type=int, default=self.stock01, metavar=self.stock01,
                          help='default stock for singles')
        self.add_argument('--stock12', type=int, default=self.stock12, metavar=self.stock12,
                          help='default stock for stacks')

        self.exclude('itemids')
        self.exclude('urls')

    def __after__(self):
        super(Options, self).__after__()

        urls = []
        for obj in self.urls:
            if isinstance(obj, list):
                urls.extend(obj)
            else:
                urls.append(obj)
        self.urls = urls

        if not self.urls:
            self.urls = None

        itemids = []
        for obj in self.itemids:
            if isinstance(obj, list):
                itemids.extend(obj)
            else:
                itemids.append(obj)
        self.itemids = itemids

        if not self.itemids:
            self.itemids = None


if __name__ == '__main__':
    pass
