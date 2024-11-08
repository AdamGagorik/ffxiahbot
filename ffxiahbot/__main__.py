"""
The script will interact with the Auction House of a private Final Fantasy XI server.
"""

import logging
import os
from logging import Handler
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Annotated

import typer
from rich.logging import RichHandler
from typer import Option, Typer

import ffxiahbot.apps.broker
import ffxiahbot.apps.clear
import ffxiahbot.apps.refill
import ffxiahbot.apps.scrub

app = Typer(
    add_completion=False,
    help=__doc__,
    invoke_without_command=True,
    rich_markup_mode="rich",
    pretty_exceptions_enable=True,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)


@app.callback()
def setup(
    version: Annotated[bool, Option("--version", help="Show version string.", is_eager=True)] = False,
    silent: Annotated[bool, Option("--silent", help="Only show ERROR messages.")] = False,
    verbose: Annotated[bool, Option("--verbose", help="Also show DEBUG messages.")] = False,
    logfile: Annotated[Path, Option(help="The path to the log file.")] = Path("ahbot.log"),
    no_logfile: Annotated[bool, Option("--disable-logfile", help="Disable logging to a file.")] = False,
) -> None:
    """
    Setup logging.
    """
    if version:
        from ffxiahbot import __version__

        print(f"ffxiahbot v{__version__}")
        typer.Exit(0)

    handlers: list[Handler] = [RichHandler()]

    if not no_logfile:
        file_handler = RotatingFileHandler(logfile, maxBytes=1048576 * 5, backupCount=5)
        file_handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s][%(processName)s][%(threadName)s][%(levelname)-5s]: %(message)s",
                "%Y-%m-%d %H:%M:%S",
            )
        )
        handlers.append(file_handler)

    logging.basicConfig(
        level=(logging.DEBUG if verbose else logging.INFO if not silent else logging.ERROR),
        format="%(message)s",
        handlers=handlers,
    )

    # disable logging from aiohttp
    if os.environ.get("FFXIAHBOT_SCRUB_DEBUG_ASYNCIO", "0").lower() not in {"1", "true"}:
        logging.getLogger("asyncio").disabled = True


app.command("broker")(ffxiahbot.apps.broker.main)
app.command("clear")(ffxiahbot.apps.clear.main)
app.command("refill")(ffxiahbot.apps.refill.main)
app.command("scrub")(ffxiahbot.apps.scrub.main)


if __name__ == "__main__":
    app()
