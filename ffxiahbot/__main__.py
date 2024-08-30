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

import ffxiahbot.apps.broker
import ffxiahbot.apps.clear
import ffxiahbot.apps.refill
import ffxiahbot.apps.scrub

OptionalPath = Optional[Path]


app = Typer(add_completion=False, help=__doc__, invoke_without_command=True, rich_markup_mode="rich")


@app.callback()
def setup(
    version: Annotated[bool, Option("--version", help="Also show DEBUG messages.", is_eager=True)] = False,
    silent: Annotated[bool, Option("--silent", help="Only show ERROR messages.")] = False,
    verbose: Annotated[bool, Option("--verbose", help="Enable verbose logging.")] = False,
    logfile: Annotated[Path, Option(help="The path to the log file.")] = Path("ahbot.log"),
    no_logfile: Annotated[bool, Option("--disable-logfile", help="Disable logging to a file.")] = False,
):
    """
    Setup logging.
    """
    if version:
        from ffxiahbot import __version__

        print(f"ffxiahbot v{__version__}")
        typer.Exit(0)

    if no_logfile:
        handlers = [RichHandler()]
    else:
        file_handler = RotatingFileHandler(logfile, maxBytes=1048576 * 5, backupCount=5)
        file_handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s][%(processName)s][%(threadName)s][%(levelname)-5s]: %(message)s", "%Y-%m-%d %H:%M:%S"
            )
        )
        handlers = [RichHandler(), file_handler]

    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO if not silent else logging.ERROR,
        format="%(message)s",
        handlers=handlers,
    )


app.command("broker")(ffxiahbot.apps.broker.main)
app.command("clear")(ffxiahbot.apps.clear.main)
app.command("refill")(ffxiahbot.apps.refill.main)
app.command("scrub")(ffxiahbot.apps.scrub.main)


if __name__ == "__main__":
    app()
