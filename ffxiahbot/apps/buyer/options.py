"""
Buy items on the auction house.
"""

from ffxiahbot.options.ah import AHOptions
from ffxiahbot.options.basic import BasicOptions
from ffxiahbot.options.input import InputOptions
from ffxiahbot.options.sql import SQLOptions


class Options(AHOptions, InputOptions, SQLOptions, BasicOptions):
    """
    Reads options from config file, then from command line.
    """

    def __init__(self):
        super().__init__(description=__doc__)
        self.tick = 30  # buying interval
        self.add_argument("--tick", type=int, default=self.tick, metavar="int", help="buying interval (seconds)")


if __name__ == "__main__":
    pass
