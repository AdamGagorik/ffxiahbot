"""
Buy and sell items on the auction house.
"""

import datetime
import time
from pathlib import Path
from typing import Annotated

from typer import Option

from ffxiahbot.config import Config
from ffxiahbot.logutils import logger


def main(
    cfg_path: Annotated[Path, Option("--config", help="Config file path.")] = Path("config.yaml"),
    inp_csvs: Annotated[list[Path], Option("--inp-csv", help="Input CSV file path.")] = (Path("items.csv"),),
    buy_items: Annotated[bool, Option(help="Enable the buying of items.")] = True,
    sell_items: Annotated[bool, Option(help="Enable the selling of items.")] = True,
):
    """
    Run a bot that buys and sells items on the auction house continuously.
    """
    from ffxiahbot.auction.manager import Manager
    from ffxiahbot.itemlist import ItemList

    config: Config = Config.from_yaml(cfg_path)
    logger.info("%s", config.model_dump_json(indent=2))

    if not buy_items and not sell_items:
        raise RuntimeError("both buying and selling are disabled! nothing to do...")

    # create auction house manager
    manager = Manager.create_database_and_manager(
        hostname=config.hostname,
        database=config.database,
        username=config.username,
        password=config.password,
        port=config.port,
        name=config.name,
        fail=config.fail,
    )

    # load data
    idata = ItemList.from_csv(*inp_csvs)

    # main loop
    logger.info("starting main loop...")
    start = datetime.datetime.now()
    last = start
    while True:
        now = datetime.datetime.now()
        delta = (now - last).total_seconds()
        elapsed = (now - start).total_seconds()
        logger.debug(
            "time=%012.1f s last restock=%012.1f s next restock=%012.1f s", elapsed, delta, config.restock - delta
        )

        if sell_items and delta >= config.restock:
            logger.debug("restocking...")
            manager.restock_items(itemdata=idata)
            last = datetime.datetime.now()

        # buy items
        if buy_items:
            manager.buy_items(itemdata=idata)

        # sleep until next tick
        logger.debug("wait=%012.1f s", config.tick)
        time.sleep(config.tick)
