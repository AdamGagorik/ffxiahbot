# -*- coding: utf-8 -*-
"""
Basic options.
"""
from .base import BaseOptions
from pydarkstar import logutils
import logging


class BasicOptions(BaseOptions):
    def __init__(self, *args, **kwargs):
        super(BasicOptions, self).__init__(*args, **kwargs)

        self.verbose = False  # error, info, and debug
        self.silent = False  # error only

        self.add_argument('--verbose', action='store_true', help='report debug, info, and error')
        self.add_argument('--silent', action='store_true', help='report error only')

    def __after__(self):
        super(BasicOptions, self).__after__()
        logutils.basic_config(verbose=self.verbose, silent=self.silent, fname='pydarkstar.log')
        self.log_values(level=logging.INFO)


if __name__ == '__main__':
    pass
