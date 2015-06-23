# -*- coding: utf-8 -*-
"""
Basic options.
"""
from ..options import BaseOptions


class BasicOptions(BaseOptions):
    def __init__(self, *args, **kwargs):
        super(BasicOptions, self).__init__(*args, **kwargs)

        self.verbose = False  # error, info, and debug
        self.silent = False  # error only

        self.add_argument('--verbose', action='store_true', help='report debug, info, and error')
        self.add_argument('--silent', action='store_true', help='report error only')


if __name__ == '__main__':
    pass
