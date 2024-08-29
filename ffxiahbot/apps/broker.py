"""
Buy and sell items on the auction house.
"""

import datetime
import time

from ffxiahbot.logutils import logger


def main():
    """
    Main function.
    """
    from ffxiahbot.apps.broker.options import Options
    from ffxiahbot.auction.manager import Manager
    from ffxiahbot.itemlist import ItemList

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

    # main loop
    logger.info("starting main loop...")
    start = datetime.datetime.now()
    last = start
    while True:
        now = datetime.datetime.now()
        delta = (now - last).total_seconds()
        elapsed = (now - start).total_seconds()
        logger.debug(
            "time=%012.1f s last restock=%012.1f s next restock=%012.1f s", elapsed, delta, opts.restock - delta
        )

        if delta >= opts.restock:
            logger.debug("restocking...")
            manager.restock_items(itemdata=idata)
            last = datetime.datetime.now()

        # buy items
        manager.buy_items(itemdata=idata)

        # sleep until next tick
        logger.debug("wait=%012.1f s", opts.tick)
        time.sleep(opts.tick)
