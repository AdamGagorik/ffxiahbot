# -*- coding: utf-8 -*-
"""
Basic options.
"""
from .base import BaseOptions


class AHOptions(BaseOptions):
    def __init__(self, *args, **kwargs):
        super(AHOptions, self).__init__(*args, **kwargs)
        self.name = 'Zissou'  # seller name
        self.add_argument('--name', type=str, default=self.name, metavar='str', help='seller name')


if __name__ == '__main__':
    pass
