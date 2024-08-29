"""
SQL options.
"""

from ffxiahbot.options.base import BaseOptions


class SQLOptions(BaseOptions):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hostname = "127.0.0.1"
        self.database = "dspdb"
        self.username = "root"
        self.password = ""
        self.fail = False  # fail on SQL errors
        self.add_argument("--hostname", default=self.hostname, type=str, metavar="str", help="SQL address")
        self.add_argument("--database", default=self.database, type=str, metavar="str", help="SQL database")
        self.add_argument("--username", default=self.username, type=str, metavar="str", help="SQL username")
        self.add_argument("--password", default=self.password, type=str, metavar="str", help="SQL password")
        self.add_argument("--fail", action="store_true", help="fail on SQL errors")
        self.exclude("password")


if __name__ == "__main__":
    pass
