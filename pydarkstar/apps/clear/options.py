# -*- coding: utf-8 -*-
"""
Clear the auction house.
"""
from ...options.basic import BasicOptions
from ...options.sql import SQLOptions
from ...options.ah import AHOptions


class Options(AHOptions, SQLOptions, BasicOptions):
    def __init__(self):
        super(Options, self).__init__(description=__doc__)
        self.force = False  # clear all items check
        self.all = False  # clear all items
        self.add_argument('--all', action='store_true', help='clear *all* items')
        self.add_argument('--force', action='store_true', help='force the item clear')


if __name__ == '__main__':
    pass
