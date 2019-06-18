import argparse
import warnings
import logging
import yaml
import os
import re

from pydarkstar.darkobject import DarkObject


class MetaOptions(type):
    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        getattr(obj, '__after__', lambda: 1)()
        return obj


class BaseOptions(DarkObject, metaclass=MetaOptions):
    regex_tuple = re.compile('([^=]+)=([^=]+)')

    def __init__(self, config='config.yaml', description=None):
        super(BaseOptions, self).__init__()
        logging.debug('BaseOptions.__init__')
        self._ordered_keys = []
        self._exclude_keys = set()

        self._parent = argparse.ArgumentParser(add_help=False)
        self._parser = argparse.ArgumentParser(parents=[self._parent],
                                               description=description,
                                               formatter_class=argparse.RawDescriptionHelpFormatter)

        # config file option
        self.config = config

        # config file
        self._parent.add_argument('--config', type=str, default=self.config, metavar=self.config,
                                  help='configuration file name')

    def __after__(self):
        results, remaining_args = self._parse_known_args()
        self._parse_config()
        self._parse_args(args=remaining_args)

    def _parse_known_args(self, args=None):
        # noinspection PyTypeChecker
        return self._parent.parse_known_args(args, namespace=self)

    def _parse_config(self):
        self.load()
        self._parser.set_defaults(**self.dict())

    # noinspection PyTypeChecker
    def _parse_args(self, args=None):
        self._parser.parse_args(args, namespace=self)

    def __setattr__(self, key, value):
        super(BaseOptions, self).__setattr__(key, value)
        if not key.startswith('_'):
            if key not in self._ordered_keys:
                self._ordered_keys.append(key)

    def __setitem__(self, key, value):
        if key not in self._ordered_keys:
            raise KeyError('unknown key : %s' % key)
        setattr(self, key, value)

    def __getitem__(self, item):
        try:
            return super(BaseOptions, self).__getattribute__(item)
        except AttributeError:
            raise KeyError('unknown key : %s' % item)

    def add_argument(self, *args, **kwargs):
        """
        Add command line info.
        """
        self._parser.add_argument(*args, **kwargs)

    def add_mutually_exclusive_group(self):
        """
        Add argument group.
        """
        return self._parser.add_mutually_exclusive_group()

    def include(self, key):
        """
        Include key for yaml.
        """
        self._exclude_keys.difference_update(key)
        self._exclude_keys.intersection_update(self._ordered_keys)

    def exclude(self, key):
        """
        Exclude key from yaml.
        """
        self._exclude_keys.add(key)
        self._exclude_keys.intersection_update(self._ordered_keys)

    def load(self, stream=None, **kwargs):
        """
        Load data from yaml.
        """
        if stream is None:
            if not os.path.exists(self.config):
                return

            self.debug('load %s', self.config)
            with open(self.config, 'rb') as handle:
                data = yaml.load(handle)

        else:
            self.debug('load %s', stream)
            data = yaml.load(stream, **kwargs)

        if data is None:
            return

        try:
            self.update(**data)
        except TypeError:
            logging.exception('yaml is invalid')
            raise RuntimeError

    def dump(self, stream=None):
        """
        Save data to yaml.
        """
        if stream is None:
            self.debug('save %s', self.config)
            with open(self.config, 'wb') as handle:
                for k in self._ordered_keys:
                    if k not in self._exclude_keys:
                        yaml.dump({k: self[k]}, handle, default_flow_style=False)
        else:
            self.debug('save %s', stream)
            for k in self._ordered_keys:
                if k not in self._exclude_keys:
                    yaml.dump({k: self[k]}, stream, default_flow_style=False)

    def update(self, **kwargs):
        """
        Update values.
        """
        for k in kwargs:
            v = kwargs[k]

            if not hasattr(self, k):
                logging.info('ignoring key in update: {}'.format(k))
            else:
                t = type(getattr(self, k))

                if not isinstance(v, t):
                    warnings.warn('key={} is {}, expecting {}'.format(
                        k, type(v).__name__, t.__name__))

                self[k] = t(v)

    def dict(self):
        """
        Return namespace as python dict.
        """
        return {k: self[k] for k in self._ordered_keys if k not in self._exclude_keys}

    def log_values(self, level=logging.DEBUG, fmt='%-10s = %s'):
        """
        Write values to logger.
        """
        for k in self.keys:
            v = self[k]
            if k in self._exclude_keys:
                self.log(level, fmt, k, '????')
            else:
                self.log(level, fmt, k, v)

    @property
    def keys(self):
        """
        Return the ordered keys.
        """
        return self._ordered_keys

    def __iter__(self):
        """
        Iterate over keys.
        """
        for k in self._ordered_keys:
            yield k

    def parse_tuple(self, string):
        # make sure string is of the form key=value
        m = self.regex_tuple.match(string)
        if not m:
            raise TypeError('can not parse string: %s' % string)

        # extract key
        k = m.group(1)

        # extract value
        try:
            v = eval(m.group(2))
        except (NameError, TypeError):
            v = m.group(2)

        # return key, value tuple
        return k, v


if __name__ == '__main__':
    opts = BaseOptions()
