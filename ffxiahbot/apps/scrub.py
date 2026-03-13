"""
Create item database.
"""

import asyncio
import csv
from pathlib import Path
from typing import Annotated, cast

from click import Choice
from typer import Exit, Option

from ffxiahbot.common import OptionalIntList, OptionalPath, OptionalStrList, progress_bar
from ffxiahbot.logutils import logger
from ffxiahbot.scrubbing.enums import ServerID

# noinspection PyProtectedMember
ServerIDOption = Option(
    "--server",
    help="The server name (asura, bahamut, etc).",
    click_type=Choice(ServerID._member_names_, case_sensitive=False),
    metavar="SERVER",
)


def _load_item_ids_from_csv(path: Path) -> list[int]:
    """Load item IDs from a CSV with an itemid column."""
    if not path.exists():
        raise FileNotFoundError(f"input CSV does not exist: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)

        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header row: {path}")

        header_map = {name.strip().lower(): name for name in reader.fieldnames}
        if "itemid" not in header_map:
            raise ValueError(
                f"CSV is missing required 'itemid' column: {path}\n"
                f"found columns: {', '.join(reader.fieldnames)}"
            )

        itemid_col = header_map["itemid"]

        item_ids: list[int] = []
        seen: set[int] = set()

        for row_num, row in enumerate(reader, start=2):
            raw = str(row.get(itemid_col, "")).strip()
            if not raw:
                continue

            try:
                item_id = int(raw)
            except ValueError:
                logger.warning("skipping non-integer itemid on row %d: %r", row_num, raw)
                continue

            if item_id not in seen:
                seen.add(item_id)
                item_ids.append(item_id)

    if not item_ids:
        raise ValueError(f"no valid item IDs found in CSV: {path}")

    return sorted(item_ids)


def main(
    cfg_path: Annotated[Path, Option("--config", help="Config file path.")] = Path("config.yaml"),
    out_csv: Annotated[Path, Option("--out-csv", help="The output CSV file to save.")] = Path("items.csv"),
    inp_csv: Annotated[
        OptionalPath,
        Option(
            "--inp-csv",
            help="Optional input CSV containing an itemid column. "
            "When provided, scrub will scrape exactly those item IDs.",
        ),
    ] = None,
    server_str: Annotated[str, ServerIDOption] = ServerID.ASURA.name,
    cat_urls: Annotated[OptionalStrList, Option("--cat-url", help="Preset category URLs.")] = None,
    item_ids: Annotated[OptionalIntList, Option("--item-id", help="Preset item IDs.")] = None,
    overwrite: Annotated[bool, Option("--overwrite", help="Overwrite output CSV?")] = False,
    stock_single: Annotated[int, Option(help="The default number of items for singles.")] = 10,
    stock_stacks: Annotated[int, Option(help="The default number of items for stacks.")] = 10,
    should_backup: Annotated[bool, Option("--backup", help="Backup output CSV?")] = False,
    cache: Annotated[OptionalPath, Option("--cache", help="A directory to cache the fetched data")] = None,
) -> None:
    """Download a list of item prices from ffxiah.com and save to a CSV file."""
    from ffxiahbot.common import backup
    from ffxiahbot.config import Config
    from ffxiahbot.itemlist import ItemList
    from ffxiahbot.scrubbing.ffxiah import FFXIAHScrubber, augment_item_info

    config: Config = Config.from_yaml(cfg_path)
    logger.info("%s", config.model_dump_json(indent=2))

    if not out_csv.suffix.lower() == ".csv":
        raise ValueError("--out-csv file must be a CSV file!")

    if inp_csv is not None and not Path(inp_csv).suffix.lower() == ".csv":
        raise ValueError("--inp-csv file must be a CSV file!")

    if not overwrite and not should_backup and out_csv.exists():
        logger.error("output file already exists!\n\t%s", out_csv)
        logger.error("please use --overwrite or --backup")
        raise Exit(-1)

    csv_item_ids: list[int] = []
    if inp_csv is not None:
        csv_item_ids = _load_item_ids_from_csv(Path(inp_csv))
        logger.info("loaded %d item IDs from %s", len(csv_item_ids), inp_csv)

    cli_item_ids = sorted(set(item_ids or []))

    # If CSV IDs are present, they become the primary reference.
    # CLI --item-id values are appended and deduped.
    merged_item_ids: list[int] | None = None
    if csv_item_ids or cli_item_ids:
        merged_item_ids = sorted(set(csv_item_ids).union(cli_item_ids))
        if cat_urls:
            logger.warning("--cat-url ignored because explicit item IDs were provided")

    scrubber = FFXIAHScrubber(
        server=cast(ServerID, ServerID[server_str.upper()]),
        cache=cache,
    )

    results, failed = asyncio.run(
        scrubber.scrub(
            cat_urls=None if merged_item_ids is not None else cat_urls,
            item_ids=merged_item_ids,
        )
    )

    if results:
        item_list = ItemList()

        with progress_bar("[red]Validate Items...", total=len(results)) as (progress, progress_task):
            for itemid in sorted(results.keys()):
                kwargs = augment_item_info(
                    results[itemid],
                    stock_single=stock_single,
                    stock_stacks=stock_stacks,
                )
                progress.update(progress_task, advance=1)
                item_list.add(itemid, **kwargs)

        if should_backup:
            backup(out_csv, copy=True)

        item_list.save_csv(out_csv)
    else:
        raise RuntimeError("no items were scrubbed!")

    if failed:
        logger.warning("failed to scrub %d item IDs", len(failed))
        raise RuntimeError("not all item ids were scrubbed, but a CSV was still saved!")
