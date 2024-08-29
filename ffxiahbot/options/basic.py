"""
Basic options.
"""

import logging

from ffxiahbot import logutils
from ffxiahbot.options.base import BaseOptions


class BasicOptions(BaseOptions):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.verbose = False  # error, info, and debug
        self.silent = False  # error only

        self.add_argument("--verbose", action="store_true", help="report debug, info, and error")
        self.add_argument("--silent", action="store_true", help="report error only")

    def __after__(self):
        super().__after__()
        logutils.basic_config(verbose=self.verbose, silent=self.silent, fname="ffxiahbot.log")
        self.log_values(level=logging.INFO)


if __name__ == "__main__":
    pass
