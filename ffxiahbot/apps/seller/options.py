"""
Sell items on the auction house.
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
        self.restock = 3600  # restock tick
        self.add_argument("--restock", type=int, default=self.restock, metavar="int", help="restock interval (seconds)")


if __name__ == "__main__":
    pass
