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

class Options(pydarkstar.options.Options):
    """
    Reads options from config file, then from command line.
    """
    def __init__(self):
        super(Options, self).__init__(config='broker.yaml', description=__doc__)

        # logging
        self.verbose = False # error, info, and debug
        self.silent  = False # error only

        # input and output
        self.save    = False # save config

        # logging
        self.add_argument('--verbose', action='store_true',
            help='report debug, info, and error')
        self.add_argument('--silent', action='store_true',
            help='report error only')

        # output
        self.add_argument('--save', action='store_true',
            help='save config file (and exit)')

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

def cleanup():
    logging.info('exit\n')

if __name__ == '__main__':
    with pydarkstar.logutils.capture():
        main()
    cleanup()