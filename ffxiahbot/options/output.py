"""
Output options.
"""

from ffxiahbot.options.base import BaseOptions


class OutputOptions(BaseOptions):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stub = "items"  # output file stub
        self.overwrite = False  # overwrite output
        self.backup = False  # backup output
        self.add_argument(dest="stub", nargs="?", type=str, default=self.stub, help="output file stub")
        self.add_argument("--overwrite", action="store_true", help="overwrite output file")
        self.add_argument("--backup", action="store_true", help="backup output file")


if __name__ == "__main__":
    pass
