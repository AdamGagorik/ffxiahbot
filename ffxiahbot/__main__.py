"""
The script will interact with the Auction House of a private Final Fantasy XI server.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.logging import RichHandler
from typer import Option, Typer

import ffxiahbot.apps.scrub

OptionalPath = Optional[Path]


app = Typer(add_completion=False, help=__doc__, invoke_without_command=True)


@app.callback()
def setup(
    version: Annotated[bool, Option(help="Show version information.", is_eager=True)] = False,
    silent: Annotated[bool, Option(help="Enable silent logging.")] = False,
    verbose: Annotated[bool, Option(help="Enable verbose logging.")] = False,
    log_file: Annotated[Path, Option(help="Log file path.")] = Path("ffxi-ah-bot.log"),
):
    """
    Setup logging.
    """
    if version:
        from ffxiahbot import __version__

        print(f"ffxiahbot v{__version__}")
        typer.Exit(0)

    handler = RotatingFileHandler(log_file, maxBytes=1048576 * 5, backupCount=5)
    handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s][%(processName)s][%(threadName)s][%(levelname)-5s]: %(message)s", "%Y-%m-%d %H:%M:%S"
        )
    )
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO if not silent else logging.ERROR,
        format="%(message)s",
        handlers=[RichHandler(), handler],
    )


app.command("scrub")(ffxiahbot.apps.scrub.main)


if __name__ == "__main__":
    app()
