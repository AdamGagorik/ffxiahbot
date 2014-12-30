"""
Create item database.
"""
import argparse
import logging
import sys
import os

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

def get_arguments(work, args=None):
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # output
    parser.add_argument(dest='ofile', nargs='?', default='items.csv',
        help='output file name')

    # scrubbing parameters
    parser.add_argument('-f', '--force', action='store_true',
        help='start from scratch')
    parser.add_argument('-t', '--threads', type=int, default=-1,
        help='number of cpu threads to use')

    # defaults
    parser.add_argument('--stock', default=5, type=int,
        help='default stock (number of items sold)')
    parser.add_argument('--stock01', default=None, type=int,
        help='default stock for singles (--stock if not given)')
    parser.add_argument('--stock12', default=None, type=int,
        help='default stock for stacks (--stock if not given)')

    # logging
    parser.add_argument('-v', '--verbose', action='store_true',
        help='logging level = 2')
    parser.add_argument('-s', '--silent', action='store_true',
        help='logging level = 0')

    opts = parser.parse_args(args)

    if opts.stock01 is None:
        opts.stock01 = opts.stock

    if opts.stock12 is None:
        opts.stock12 = opts.stock

    return opts

def setup_logging(opts):
    pydarkstar.logutils.setInfo()

    if opts.verbose:
        pydarkstar.logutils.setDebug()

    if opts.silent:
        pydarkstar.logutils.setError()

    pydarkstar.logutils.addRotatingFileHandler(fname='scrub.log')
    logging.info('start')

def main():
    work = os.getcwd()
    opts = get_arguments(work)
    setup_logging(opts)
    scrubber = pydarkstar.scrub.ffxiah.FFXIAHScrubber()
    data = scrubber.scrub(force=opts.force, threads=opts.threads, ids=[1, 2, 3])
    ilist = pydarkstar.itemlist.ItemList()
    for itemid in data:

        try:
            price01, sell01 = data[itemid]['median'], True
        except KeyError:
            price01, sell01 = None, False

        try:
            price12, sell12 = data[itemid]['stack price'], True
        except KeyError:
            price12, sell12 = None, False

        try:
            name = data[itemid]['name']
        except KeyError:
            name=None

        ilist.add(itemid, name=name,
            price01=price01, stock01=opts.stock01, sell01=sell01, buy01=True,
            price12=price12, stock12=opts.stock12, sell12=sell12, buy12=True)

    ilist.savecsv(opts.ofile)

def cleanup():
    logging.info('exit\n')

if __name__ == '__main__':
    with pydarkstar.logutils.capture():
        main()
    cleanup()
