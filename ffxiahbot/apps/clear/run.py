"""
Clear the auction house.
"""

import logging

from ffxiahbot import logutils
from ffxiahbot.apps.clear.options import Options
from ffxiahbot.auction.manager import Manager


def main():
    """
    Main function.
    """
    # get options
    opts = Options()

    # create auction house manager
    manager = Manager.create_database_and_manager(
        hostname=opts.hostname,
        database=opts.database,
        username=opts.username,
        password=opts.password,
        name=opts.name,
        fail=opts.fail,
    )

    # clear all items
    if opts.all:
        # really?
        if not opts.force:
            raise RuntimeError("clearing all items from auction house is dangerous. use --force")
        else:
            manager.cleaner.clear(seller=None)
    # clear seller items
    else:
        if not opts.force:
            raise RuntimeError("clearing all items from auction house is dangerous. use --force")
        else:
            manager.cleaner.clear(seller=manager.seller.seller)

    # exit after clearing
    logging.info("exit after clear")
    return


def cleanup():
    logging.info("exit\n")


if __name__ == "__main__":
    with logutils.capture():
        main()
    cleanup()
