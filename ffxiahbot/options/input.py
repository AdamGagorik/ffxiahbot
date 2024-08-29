"""
Input options.
"""

from ffxiahbot.options.base import BaseOptions


class InputOptions(BaseOptions):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = []  # list of itemdata
        self.add_argument(
            dest="data", nargs="*", type=str, default=self.data, metavar="str", help="item data CSV file(s)"
        )

    def __after__(self):
        super().__after__()
        self.data = list(set(self.data))


if __name__ == "__main__":
    pass
