"""
Buy and sell items on the auction house.
"""

from datetime import datetime
from pathlib import Path
from typing import Annotated, Any

from apscheduler.schedulers.blocking import BlockingScheduler
from typer import Option

from ffxiahbot.common import OptionalPath, OptionalPathList
from ffxiahbot.config import Config
from ffxiahbot.database import Database
from ffxiahbot.logutils import logger
from ffxiahbot.tables.base import Base


def main(
    cfg_path: Annotated[Path, Option("--config", help="Config file path.")] = Path("config.yaml"),
    inp_csvs: Annotated[
        OptionalPathList, Option("--inp-csv", help="Input CSV file path.", show_default="items.csv")
    ] = None,
    buy_items: Annotated[bool, Option(help="Enable the buying of items.")] = True,
    sell_items: Annotated[bool, Option(help="Enable the selling of items.")] = True,
    buy_immediately: Annotated[
        bool, Option("--buy-immediately", help="Buy items immediately instead of waiting?")
    ] = False,
    restock_immediately: Annotated[
        bool, Option("--restock-immediately", help="Restock items immediately instead of waiting?")
    ] = False,
    use_sqlite_db: Annotated[OptionalPath, Option(help="Use a test SQLite database instead of the real one?")] = None,
) -> None:
    """
    Run a bot that buys and sells items on the auction house continuously.
    """
    from ffxiahbot.auction.manager import Manager
    from ffxiahbot.itemlist import ItemList

    if inp_csvs is None:
        inp_csvs = [Path("items.csv")]

    config: Config = Config.from_yaml(cfg_path)
    logger.info("%s", config.model_dump_json(indent=2))

    if not buy_items and not sell_items:
        raise RuntimeError("both buying and selling are disabled! nothing to do...")

    # create auction house manager
    if use_sqlite_db:
        manager = Manager.from_db(
            db=Database.sqlite(database=str(use_sqlite_db)),
            name=config.name,
            fail=config.fail,
        )
        Base.metadata.create_all(manager.db.engine)
    else:
        manager = Manager.create_database_and_manager(
            hostname=config.hostname,
            database=config.database,
            username=config.username,
            password=config.password,
            port=config.port,
            name=config.name,
            fail=config.fail,
        )

    # test database connection
    if not manager.can_connect():
        raise RuntimeError("cannot connect to the database!")

    # load data
    item_list = ItemList.from_csv(*inp_csvs)

    # run callbacks on a schedule
    scheduler = BlockingScheduler()

    if buy_items:
        buy_kwargs: dict[str, Any] = {} if not buy_immediately else {"next_run_time": datetime.now().astimezone()}
        scheduler.add_job(
            lambda: manager.buy_items(item_list=item_list, use_buying_rates=config.use_buying_rates),
            trigger="interval",
            id="buy_items",
            seconds=config.tick,
            max_instances=1,
            name="Buy Items",
            **buy_kwargs,
        )

    if sell_items:
        sell_kwargs: dict[str, Any] = {} if not restock_immediately else {"next_run_time": datetime.now().astimezone()}
        scheduler.add_job(
            lambda: manager.restock_items(item_list=item_list, use_selling_rates=config.use_selling_rates),
            trigger="interval",
            id="restock_items",
            seconds=config.restock,
            max_instances=1,
            next_run_time=None if not restock_immediately else datetime.now().astimezone(),
            name="Restock Items",
            **sell_kwargs,
        )

    scheduler.start()
