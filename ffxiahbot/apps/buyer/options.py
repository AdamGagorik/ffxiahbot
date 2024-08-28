# -*- coding: utf-8 -*-
"""
Buy items on the auction house.
"""
from ...options.basic import BasicOptions
from ...options.input import InputOptions
from ...options.sql import SQLOptions
from ...options.ah import AHOptions


class Options(AHOptions, InputOptions, SQLOptions, BasicOptions):
    """
    Reads options from config file, then from command line.
    """
    def __init__(self):
        super(Options, self).__init__(description=__doc__)
        self.tick = 30  # buying interval
        self.add_argument('--tick', type=int, default=self.tick, metavar='int', help='buying interval (seconds)')


if __name__ == '__main__':
    pass
