"""
Clear the auction house.
"""

from pathlib import Path
from typing import Annotated

from typer import Option, confirm

from ffxiahbot.config import Config
from ffxiahbot.logutils import logger


def main(
    cfg_path: Annotated[Path, Option("--config", help="Config file path.")] = Path("config.yaml"),
    no_prompt: Annotated[bool, Option("--no-prompt", help="Do not ask for confirmation.")] = False,
    clear_all: Annotated[bool, Option("--all", help="Clear all items.")] = False,
):
    """
    Delete items from the auction house ([red]dangerous operation![/]).
    """
    from ffxiahbot.auction.manager import Manager

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

    # clear all items
    if clear_all:
        # really?
        if no_prompt or confirm("Clear all items?", abort=True, show_default=True):
            manager.cleaner.clear(seller=None)
    # clear seller items
    else:
        if no_prompt or confirm(f"Clear {config.name}'s items?", abort=True, show_default=True):
            manager.cleaner.clear(seller=manager.seller.seller)
