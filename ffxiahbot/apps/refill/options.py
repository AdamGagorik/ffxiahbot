"""
Refill the auction house.
"""

from ffxiahbot.options.ah import AHOptions
from ffxiahbot.options.basic import BasicOptions
from ffxiahbot.options.input import InputOptions
from ffxiahbot.options.sql import SQLOptions


class Options(AHOptions, InputOptions, SQLOptions, BasicOptions):
    def __init__(self):
        super().__init__(description=__doc__)
        self.force = False  # refill all items check
        self.add_argument("--force", action="store_true", help="force the item refill")


if __name__ == "__main__":
    pass
