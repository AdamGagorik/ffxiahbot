import asyncio
import logging
from dataclasses import dataclass
from typing import Any

import aiohttp
import bs4
from bs4 import BeautifulSoup

TIMEOUT: int = 1024


@dataclass()
class Scrubber:
    # noinspection PyBroadException
    @staticmethod
    async def soup(session: aiohttp.ClientSession, url: str, **kwargs: Any) -> BeautifulSoup:
        """
        Open URL and create tag soup.

        Parameters:
            session: client session
            url: website string to open
        """
        max_tries = 10
        for i in range(max_tries):
            # noinspection PyPep8
            try:
                async with session.get(url, **kwargs) as response:
                    text = await response.text()
                break
            except Exception:
                logging.exception("urlopen failed (attempt %d)", i + 1)
                if i == max_tries - 1:
                    logging.exception("the maximum urlopen attempts have been reached")
                    raise
                await asyncio.sleep(1)

        try:
            s = BeautifulSoup(text, features="html5lib")
        except bs4.FeatureNotFound:
            s = BeautifulSoup(text, features="html.parser")

        return s
