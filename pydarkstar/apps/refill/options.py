# -*- coding: utf-8 -*-
"""
Refill the auction house.
"""
from ...options.basic import BasicOptions
from ...options.input import InputOptions
from ...options.sql import SQLOptions
from ...options.ah import AHOptions


class Options(AHOptions, InputOptions, SQLOptions, BasicOptions):
    def __init__(self):
        super(Options, self).__init__(description=__doc__)
        self.force = False  # refill all items check
        self.add_argument('--force', action='store_true', help='force the item refill')


if __name__ == '__main__':
    pass
