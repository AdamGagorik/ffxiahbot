"""
Refill the auction house.
"""

from pathlib import Path
from typing import Annotated

from typer import Option, confirm

from ffxiahbot.config import Config
from ffxiahbot.logutils import logger


def main(
    cfg_path: Annotated[Path, Option("--config", help="Config file path.")] = Path("config.yaml"),
    inp_csvs: Annotated[list[Path], Option("--inp-csv", help="Input CSV file path.")] = (Path("items.csv"),),
    no_prompt: Annotated[bool, Option("--no-prompt", help="Do not ask for confirmation.")] = False,
):
    """
    Refill the auction house with the items defined in the CSV file.
    """
    from ffxiahbot.auction.manager import Manager
    from ffxiahbot.itemlist import ItemList

    config: Config = Config.from_yaml(cfg_path)
    logger.info("%s", config.model_dump_json(indent=2))

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

    if no_prompt or confirm("Restock all items?", abort=True, show_default=True):
        logger.info("restocking...")
        manager.restock_items(itemdata=idata)
        logger.info("exit after restock")
