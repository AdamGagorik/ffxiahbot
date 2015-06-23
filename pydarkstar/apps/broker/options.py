# -*- coding: utf-8 -*-
"""
Buy and sell items on the auction house.
"""
from ... import options


class Options(options.Options):
    """
    Reads options from config file, then from command line.
    """

    def __init__(self):
        super(Options, self).__init__(config='broker.yaml', description=__doc__)

        # logging
        self.verbose = False  # error, info, and debug
        self.silent = False  # error only

        # input
        self.data = []  # list of itemdata

        # sql
        self.hostname = '127.0.0.1'
        self.database = 'dspdb'
        self.username = 'root'
        self.password = ''
        self.fail = False  # fail on SQL errors

        # selling
        self.name = 'Zissou'  # seller name
        self.restock = 3600  # restock tick
        self.refill = False  # restock at start

        # buying
        self.tick = 30  # buying interval

        # logging
        self.add_argument('--verbose', action='store_true',
                          help='report debug, info, and error')
        self.add_argument('--silent', action='store_true',
                          help='report error only')

        # input
        self.add_argument(dest='data', nargs='*', type=str, default=self.data,
                          metavar='str', help='item data CSV file(s)')

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
        self.data = list(set(self.data))


if __name__ == '__main__':
    pass
