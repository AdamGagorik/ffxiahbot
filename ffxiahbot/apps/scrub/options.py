"""
Create item database.
"""

from ffxiahbot.options.basic import BasicOptions
from ffxiahbot.options.output import OutputOptions
from ffxiahbot.scrubbing.ffxiah import SERVER_ID


class Options(OutputOptions, BasicOptions):
    """
    Reads options from config file, then from command line.
    """

    def __init__(self):
        super().__init__(description=__doc__)
        self.stock_single = 10  # default stock for singles
        self.stock_stacks = 10  # default stock for stacks
        self.itemids = []  # a list of item ids
        self.threads = -1
        self.server = 1
        self.urls = []  # a list of category urls

        self.add_argument(
            "--urls",
            type=str,
            nargs="*",
            action="append",
            default=self.urls,
            metavar="url",
            help="a list of category urls",
        )
        self.add_argument(
            "--itemids",
            type=int,
            nargs="*",
            action="append",
            default=self.itemids,
            metavar="itemids",
            help="a list of item ids",
        )
        self.add_argument(
            "--stock_single",
            type=int,
            default=self.stock_single,
            metavar=self.stock_single,
            help="default stock for singles",
        )
        self.add_argument(
            "--stock_stacks",
            type=int,
            default=self.stock_stacks,
            metavar=self.stock_stacks,
            help="default stock for stacks",
        )
        self.add_argument(
            "--threads", type=int, default=-1, metavar="int", help="the number of threads (default is CPU dependent)"
        )
        self.add_argument(
            "--server",
            type=str,
            metavar="str | int",
            help="the name of the FFXI server to scrub (ex: bahamut)\n"
            "this can be a string or a number between 1 and 32",
        )

        self.exclude("itemids")
        self.exclude("urls")

    def __after__(self):  # noqa: C901
        super().__after__()

        urls = []
        for obj in self.urls:
            if isinstance(obj, list):
                urls.extend(obj)
            else:
                urls.append(obj)
        self.urls = urls

        if not self.urls:
            self.urls = None

        itemids = []
        for obj in self.itemids:
            if isinstance(obj, list):
                itemids.extend(obj)
            else:
                itemids.append(obj)
        self.itemids = itemids

        if not self.itemids:
            self.itemids = None

        try:
            self.server = int(self.server)
            if self.server not in SERVER_ID.values():
                for server, server_id in SERVER_ID.items():
                    self.error("--server %2d is %s", server_id, server)
                self.fatal("unknown --server selected: %s", self.server)
        except ValueError:
            self.server = str(self.server).lower()
            if self.server not in SERVER_ID:
                for server, server_id in SERVER_ID.items():
                    self.error("--server %2d is %s", server_id, server)
                self.fatal("unknown --server selected: %s", self.server)


if __name__ == "__main__":
    pass
