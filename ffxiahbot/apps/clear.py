"""
Clear the auction house.
"""

from ffxiahbot.logutils import logger


def main():
    """
    Main function.
    """
    from ffxiahbot.apps.clear.options import Options
    from ffxiahbot.auction.manager import Manager

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
    logger.info("exit after clear")
    return
