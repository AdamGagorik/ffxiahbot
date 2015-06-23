# -*- coding: utf-8 -*-
"""
Clear the auction house.
"""
from ..basicoptions import BasicOptions
from ..sqloptions import SQLOptions
from ..ahoptions import AHOptions


class Options(AHOptions, SQLOptions, BasicOptions):
    def __init__(self):
        super(Options, self).__init__(description=__doc__)
        self.force = False  # clear all items check
        self.all = False  # clear all items
        self.add_argument('--all', action='store_true', help='clear *all* items')
        self.add_argument('--force', action='store_true', help='force the item clear')


if __name__ == '__main__':
    pass
