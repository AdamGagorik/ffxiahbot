"""
Refill the auction house.
"""

from pathlib import Path
from typing import Annotated

from typer import Option, confirm

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
    no_prompt: Annotated[bool, Option("--no-prompt", help="Do not ask for confirmation.")] = False,
    use_sqlite_db: Annotated[OptionalPath, Option(help="Use a test SQLite database instead of the real one?")] = None,
) -> None:
    """
    Refill the auction house with the items defined in the CSV file.
    """
    from ffxiahbot.auction.manager import Manager
    from ffxiahbot.itemlist import ItemList

    if inp_csvs is None:
        inp_csvs = [Path("items.csv")]

    config: Config = Config.from_yaml(cfg_path)
    logger.info("%s", config.model_dump_json(indent=2))

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

    # load data
    item_list = ItemList.from_csv(*inp_csvs)

    if no_prompt or confirm("Restock all items?", abort=True, show_default=True):
        logger.info("restocking...")
        manager.restock_items(item_list=item_list)
        logger.info("exit after restock")
