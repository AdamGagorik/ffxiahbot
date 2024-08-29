"""
Refill the auction house.
"""

import logging

from ffxiahbot import logutils
from ffxiahbot.apps.refill.options import Options
from ffxiahbot.auction.manager import Manager
from ffxiahbot.itemlist import ItemList


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

    # load data
    idata = ItemList.from_csv(*opts.data)

    if not opts.force:
        raise RuntimeError("refilling all items from auction house is dangerous. use --force")
    else:
        logging.info("restocking...")
        manager.restock_items(itemdata=idata)
        logging.info("exit after restock")
        return


def cleanup():
    logging.info("exit\n")


if __name__ == "__main__":
    with logutils.capture():
        main()
    cleanup()
