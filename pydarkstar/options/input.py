# -*- coding: utf-8 -*-
"""
Input options.
"""
from .base import BaseOptions


class InputOptions(BaseOptions):
    def __init__(self, *args, **kwargs):
        super(InputOptions, self).__init__(*args, **kwargs)
        self.data = []  # list of itemdata
        self.add_argument(dest='data', nargs='*', type=str, default=self.data, metavar='str',
                          help='item data CSV file(s)')

    def __after__(self):
        super(InputOptions, self).__after__()
        self.data = list(set(self.data))


if __name__ == '__main__':
    pass
