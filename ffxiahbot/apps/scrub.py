"""
Create item database.
"""

import asyncio
from pathlib import Path
from typing import Annotated, cast

from click import Choice
from typer import Exit, Option

from ffxiahbot.common import OptionalIntList, OptionalPath, OptionalStrList
from ffxiahbot.logutils import logger
from ffxiahbot.scrubbing.enums import ServerID

# noinspection PyProtectedMember
ServerIDOption = Option(
    "--server",
    help="The server name (asura, bahamut, etc).",
    click_type=Choice(ServerID._member_names_, case_sensitive=False),
    metavar="SERVER",
)


def main(
    cfg_path: Annotated[Path, Option("--config", help="Config file path.")] = Path("config.yaml"),
    out_csv: Annotated[Path, Option("--out-csv", help="The output CSV file to save.")] = Path("items.csv"),
    server_str: Annotated[str, ServerIDOption] = ServerID.ASURA.name,
    cat_urls: Annotated[OptionalStrList, Option("--cat-url", help="Preset category URLs.")] = None,
    item_ids: Annotated[OptionalIntList, Option("--item-id", help="Preset item IDs.")] = None,
    overwrite: Annotated[bool, Option("--overwrite", help="Overwrite output CSV?")] = False,
    stock_single: Annotated[int, Option(help="The default number of items for singles.")] = 10,
    stock_stacks: Annotated[int, Option(help="The default number of items for stacks.")] = 10,
    should_backup: Annotated[bool, Option("--backup", help="Backup output CSV?")] = False,
    cache: Annotated[OptionalPath, Option("--cache", help="A directory to cache the fetched data")] = None,
) -> None:
    """
    Download a list of item prices from ffxiah.com and save to a CSV file.
    """
    from ffxiahbot.common import backup
    from ffxiahbot.config import Config
    from ffxiahbot.itemlist import ItemList
    from ffxiahbot.scrubbing.ffxiah import FFXIAHScrubber, augment_item_info

    config: Config = Config.from_yaml(cfg_path)
    logger.info("%s", config.model_dump_json(indent=2))

    # check output file name validity
    if not out_csv.suffix.lower() == ".csv":
        raise ValueError("--out-csv file must be a CSV file!")

    if not overwrite and not should_backup and out_csv.exists():
        logger.error("output file already exists!\n\t%s", out_csv)
        logger.error("please use --overwrite or --backup")
        raise Exit(-1)

    # scrub data
    scrubber = FFXIAHScrubber(server=cast(ServerID, ServerID[server_str.upper()]), cache=cache)
    results, failed = asyncio.run(scrubber.scrub(cat_urls=cat_urls, item_ids=item_ids))

    if results:
        # create item list from data
        item_list = ItemList()
        for itemid in sorted(results.keys()):
            kwargs = augment_item_info(results[itemid], stock_single=stock_single, stock_stacks=stock_stacks)
            item_list.add(itemid, **kwargs)

        # backup file
        if should_backup:
            backup(out_csv, copy=True)

        # overwrites if exists, but we checked already
        item_list.save_csv(out_csv)
    else:
        raise RuntimeError("no items were scrubbed!")

    if failed:
        raise RuntimeError("not all item ids were scrubbed, but a CSV was still saved!")
