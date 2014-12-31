"""
Create item database.
"""
import argparse
import logging
import yaml
import sys
import os
import re

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
import pydarkstar.darkobject

class Options(pydarkstar.darkobject.DarkObject):
    """
    Program options.
    """
    def __init__(self, args=None):
        super(Options, self).__init__()
        self.config  =  'scrub.yaml' # options in config file
        self.stub    =  'items'      # output file stub
        self.force   =  False        # redownload
        self.threads = -1            # cpu threads during download
        self.stock01 =  5            # default stock for singles
        self.stock12 =  5            # default stock for stacks
        self.verbose =  False        # logging level (debug + info + error)
        self.silent  =  False        # logging level (error)

        self._parent = argparse.ArgumentParser(add_help=False)
        self._parser = argparse.ArgumentParser(parents=[self._parent],
            description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

        # config file
        self._parent.add_argument('--config', type=str,
            default=self.config, metavar=self.config,
            help='configuration file name')

        # output
        self._parser.add_argument(dest='stub', nargs='?', type=str,
            default=self.stub, help='output file stub')

        # scrubbing parameters
        self._parser.add_argument('--force', action='store_true',
            help='start from scratch')
        self._parser.add_argument('--threads', type=int,
            default=self.threads, metavar=self.threads,
            help='number of cpu threads to use')

        # defaults
        self._parser.add_argument('--stock01', type=int,
            default=self.stock01, metavar=self.stock01,
            help='default stock for singles')
        self._parser.add_argument('--stock12', type=int,
            default=self.stock12, metavar=self.stock12,
            help='default stock for stacks')

        # logging
        self._parser.add_argument('--verbose', action='store_true',
            help='logging level = 2')
        self._parser.add_argument('--silent', action='store_true',
            help='logging level = 0')

        self._parse_args(args)

    def update(self, **kwargs):
        """
        Update options.
        """
        for k in kwargs:
            if hasattr(self, k):
                setattr(self, k, kwargs[k])
            else:
                raise KeyError('unknown option: %s', k)

    def show(self):
        """
        Show parameters in log.
        """
        fmt = '%-8s = %s'
        self.debug(fmt, 'config', self.config)
        self.debug(fmt, 'verbose', self.verbose)
        self.debug(fmt, 'silent', self.silent)
        self.debug(fmt, 'stub', self.stub)
        self.debug(fmt, 'force', self.force)
        self.debug(fmt, 'threads', self.threads)
        self.debug(fmt, 'stock01', self.stock01)
        self.debug(fmt, 'stock12', self.stock12)

    def _parse_args(self, args=None):
        """
        Parse config file and then command line.
        """
        results, remaining_args = self._parent.parse_known_args(args)
        self.update(**results.__dict__)
        self._load_config()
        results = self._parser.parse_args(remaining_args)
        self.update(**results.__dict__)
        self._save_config()

    def _load_config(self):
        """
        Parse config file.
        """
        if os.path.exists(self.config):
            self.info('load %s', self.config)
            with open(self.config, 'rb') as handle:
                data = yaml.load(handle)
                if not isinstance(data, dict):
                    raise RuntimeError('invalid configuration file')
                self.update(**data)
                self._parser.set_defaults(**data)

    def _save_config(self):
        """
        Save config file.
        """
        with open(self.config, 'wb') as handle:
            yaml.dump(self._to_dict(), handle, default_flow_style=False)

    def _to_dict(self):
        return dict(stub=self.stub, force=self.force, threads=self.threads, verbose=self.verbose,
            silent=self.silent, stock01=self.stock01, stock12=self.stock12)

def setup_logging(opts):
    pydarkstar.logutils.setInfo()

    if opts.verbose:
        pydarkstar.logutils.setDebug()

    if opts.silent:
        pydarkstar.logutils.setError()

    pydarkstar.logutils.addRotatingFileHandler(fname='scrub.log')
    logging.info('start')

def main():
    opts = Options()
    setup_logging(opts)
    opts.show()
    scrubber = pydarkstar.scrub.ffxiah.FFXIAHScrubber()
    data = scrubber.scrub(force=opts.force, threads=opts.threads)
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

    oname = '{}.csv'.format(re.sub(r'\.csv$', '', opts.stub))
    if os.path.exists(oname):
        logging.error('file already exists! %s', oname)

    ilist.savecsv(oname)

def cleanup():
    logging.info('exit\n')

if __name__ == '__main__':
    with pydarkstar.logutils.capture():
        main()
    cleanup()
