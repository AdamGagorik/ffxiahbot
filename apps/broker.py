"""
Alter item database.
"""
import logging
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
import pydarkstar.options
import pydarkstar.common

import pydarkstar.database
import pydarkstar.auction.buyer
import pydarkstar.auction.seller
import pydarkstar.auction.cleaner
import pydarkstar.auction.browser

class Options(pydarkstar.options.Options):
    """
    Reads options from config file, then from command line.
    """
    def __init__(self):
        super(Options, self).__init__(config='broker.yaml', description=__doc__)

        # logging
        self.verbose  = False # error, info, and debug
        self.silent   = False # error only

        # input and output
        self.save     = False # save config

        # sql
        self.hostname = '127.0.0.1'
        self.database = 'dspdb'
        self.username = 'root'
        self.password = None

        # logging
        self.add_argument('--verbose', action='store_true',
            help='report debug, info, and error')
        self.add_argument('--silent', action='store_true',
            help='report error only')

        # output
        self.add_argument('--save', action='store_true',
            help='save config file (and exit)')

        # sql
        self.add_argument('--hostname', default=self.hostname, type=str,
            metavar=self.hostname, help='SQL address')
        self.add_argument('--database', default=self.database, type=str,
            metavar=self.database, help='SQL database')
        self.add_argument('--username', default=self.username, type=str,
            metavar=self.username, help='SQL username')
        self.add_argument('--password', default=self.password, type=str,
            metavar='???', help='SQL password')
        self.exclude('password')

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

def cleanup():
    logging.info('exit\n')

if __name__ == '__main__':
    with pydarkstar.logutils.capture():
        main()
    cleanup()