# -*- coding: utf-8 -*-
"""
Create item database.
"""
from ... import options


class Options(options.Options):
    """
    Reads options from config file, then from command line.
    """

    def __init__(self):
        super(Options, self).__init__(config='config.yaml', description=__doc__)
        self.verbose = False  # error, info, and debug
        self.silent = False  # error only
        self.stub = 'items'  # output file stub
        self.overwrite = False  # overwrite output
        self.backup = False  # backup output
        self.force = False  # redownload
        self.pkl = False  # save pkl files
        self.threads = -1  # cpu threads during download
        self.stock01 = 5  # default stock for singles
        self.stock12 = 5  # default stock for stacks
        self.itemids = []  # a list of item ids
        self.urls = []  # a list of category urls

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

        # scrub parameters
        self.add_argument('--force', action='store_true',
                          help='start from scratch')
        self.add_argument('--pkl', action='store_true',
                          help='save pkl files')
        self.add_argument('--threads', type=int, default=self.threads, metavar=self.threads,
                          help='number of cpu threads to use')
        self.add_argument('--urls', type=str, nargs='*', action='append', default=self.urls, metavar='url',
                          help='a list of category urls')
        self.add_argument('--itemids', type=int, nargs='*', action='append', default=self.itemids, metavar='itemids',
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
