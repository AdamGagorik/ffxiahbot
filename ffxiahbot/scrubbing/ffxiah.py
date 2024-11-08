from __future__ import annotations

import asyncio
import contextlib
import json
import re
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import chain
from pathlib import Path
from typing import Any, cast

import aiohttp
from bs4 import Tag

from ffxiahbot.common import OptionalPath, progress_bar
from ffxiahbot.logutils import logger
from ffxiahbot.scrubbing.enums import ServerID
from ffxiahbot.scrubbing.scrubber import Scrubber

REGEX_CATEGORY: re.Pattern = re.compile(r"/browse/(\d+)/?.*")
REGEX_ITEM: re.Pattern = re.compile(r"/item/(\d+)")
REGEX_NAME: re.Pattern = re.compile(r"(.*?)\s*-?\s*(FFXIAH)?\.(com)?")


FailedType = dict[int, Exception]
ResultType = dict[int, dict[str, Any]]
ItemIDsType = list[int] | set[int] | tuple[int, ...]
CatURLsType = list[str] | set[str] | tuple[str, ...]


@dataclass()
class FFXIAHScrubber(Scrubber):
    """
    Get item data from the ffxiah.com website.
    """

    #: The FFXI server
    server: ServerID = ServerID.BAHAMUT
    #: The cache directory
    cache: OptionalPath = None

    async def scrub(
        self,
        cat_urls: CatURLsType | None = None,
        item_ids: ItemIDsType | None = None,
    ) -> tuple[ResultType, FailedType]:
        """
        Get item metadata main function.

        The item ids can be loaded from category urls or simply passed as a list.  The urls
        can be generated automatically, in which case all possible items will be downloaded.

        Args:
            cat_urls: A preset list of category URLs.
            item_ids: A preset list of item IDs.

        Returns:
            failed: failed item ids
            data: item data
        """
        async with aiohttp.ClientSession() as session:
            if not item_ids:
                if not cat_urls:
                    cat_urls = await self._get_category_urls(session)

                logger.debug("# urls = %d", len(cat_urls))
                item_ids = await self._get_item_ids(session, cat_urls)
            else:
                logger.debug("using passed ids")
                item_ids = sorted(set(item_ids))

                if cat_urls:
                    logger.warning("passed urls ignored")

            results, failed = await self._get_item_data(session, item_ids)
            logger.debug("expect count = %d", len(item_ids))
            logger.debug("passed count = %d", len(results))
            logger.debug("failed count = %d", len(failed))

            return results, failed

    # step 1
    async def _get_category_urls(self, session: aiohttp.ClientSession) -> list[str]:
        """
        Parse http://www.ffxiah.com/browse to get URLs of the form http://www.ffxiah.com/{CategoryNumber}.
        """
        logger.debug("getting category urls")

        # the browse section of FFXIAH has a list of urls with category numbers
        logger.debug("open %s", path := "http://www.ffxiah.com/browse")
        soup = await self.soup(session, path)

        def _() -> Iterable[str]:
            for tag in soup.find_all("a"):
                if tag.has_attr("href"):
                    href = tag.get("href")
                    match = REGEX_CATEGORY.match(href)
                    if match:
                        try:
                            category = int(match.group(1))
                            if category < 240:
                                yield f"http://www.ffxiah.com{href}"
                                logger.debug("category %s", href)
                            else:
                                logger.debug("skipping %s", href)

                        except (ValueError, IndexError):
                            logger.exception("failed to extract category")
                    else:
                        logger.debug("ignoring %s", href)

        return sorted(_(), key=lambda x: list(map(float, re.findall(r"\d+", x))))

    # step 2
    async def _get_item_ids(self, session: aiohttp.ClientSession, urls: CatURLsType) -> list[int]:
        """
        Scrub urls of the form http://www.ffxiah.com/{CategoryNumber} for itemids.
        """
        tasks = []
        logger.info("getting itemids")
        for i, cat_url in enumerate(urls):
            logger.info("category %02d/%02d : %s", i + 1, len(urls), cat_url)
            tasks.append(asyncio.create_task(self._get_itemids_for_category_url(session, cat_url)))

        return sorted(set(chain(*await asyncio.gather(*tasks))))

    # step 2.1
    async def _get_itemids_for_category_url(self, session: aiohttp.ClientSession, url: str) -> Iterable[int]:
        """
        Scrub url of the form http://www.ffxiah.com/{CategoryNumber} for itemids.
        """
        # create tag soup
        soup = await self.soup(session, url)

        def _() -> Iterable[int]:
            # look for table class
            table = soup.find("table", class_="stdlist")
            if not table:
                logger.error("failed to parse <table>")
                return

            # look for table body
            tbody = table.find("tbody")
            if not tbody:
                logger.error("failed to parse <tbody>")
                return

            # look for table rows
            trs = cast(Tag, tbody).find_all("tr")
            if not trs:
                logger.error("failed to parse <tr>")
                return

            # loop table rows
            count = 0
            for j, row in enumerate(trs):
                # look for 'a' tag
                a = row.find("a")

                if a is not None:
                    # look for href attr
                    href = a.get("href")

                    if href is not None:
                        # make sure href matches /item/{number}
                        if (match := REGEX_ITEM.match(href)) is None:
                            logger.error("failed to extract itemid!\n\n\trow %d of %s\n\n%s\n\n", j, url, row)
                        else:
                            item = int(match.group(1))
                            count += 1
                            yield item
                    else:
                        logger.error("failed to extract href!\n\n\trow %d of %s\n\n%s\n\n", j, url, row)
                else:
                    logger.error("failed to extract 'a' tag!\n\n\trow %d of %s\n\n%s\n\n", j, url, row)

            # make sure we found something
            if not count:
                logger.error("could not find any itemids!")

        return set(_())

    # step 3
    async def _get_item_data(self, session: aiohttp.ClientSession, itemids: list[int]) -> tuple[ResultType, FailedType]:
        """
        Get metadata for many items.
        """
        logger.info("getting data")
        tasks = {
            itemid: asyncio.create_task(self._get_item_data_for_itemid(session, itemid, index=i, total=len(itemids)))
            for i, itemid in enumerate(itemids)
        }

        results, failed = {}, {}
        with progress_bar("[red]Fetching Items...", total=len(itemids)) as (progress, progress_task):
            for i, (itemid, task) in enumerate(tasks.items()):
                progress.update(progress_task, advance=1)
                # noinspection PyBroadException
                try:
                    results[itemid] = await task
                    logger.info("item %06d/%06d : %06d", i, len(itemids), itemid)
                except Exception as e:
                    failed[itemid] = e
                    logger.error("item %06d/%06d : %06d", i, len(itemids), itemid)
                    pass

        return results, failed

    def _cache_sub(self, itemid: int) -> Path:
        """
        Create cache subdirectory.
        """
        if self.cache is None:
            raise RuntimeError("cache is not set!")

        return cast(Path, self.cache).joinpath(f"{self.server.value}", f"{itemid // 1000}", f"{itemid}")

    # step 3.1
    async def _get_item_data_for_itemid(
        self, session: aiohttp.ClientSession, itemid: int, index: int = 0, total: int = 0
    ) -> dict[str, Any]:
        """
        Get metadata for single item.
        """
        percent = float(index) / float(total) * 100.0 if total > 0 else 0.0

        data: dict[str, Any] = {"name": None, "itemid": itemid}
        url = f"http://www.ffxiah.com/item/{itemid}"

        # load cache
        if self.cache is not None:
            cache_stub = self._cache_sub(itemid)
            if (cache_path := cache_stub.with_suffix(".json")).exists():
                logger.debug("load server=%s (%06d/%06d,%6.2f) %s", self.server, index, total, percent, url)
                return cast(dict[str, Any], json.loads(cache_path.read_text()))

        # create tag soup
        logger.debug("open server=%s (%06d/%06d,%6.2f) %s", self.server, index, total, percent, url)
        soup = await self.soup(session, url, data={"sid": self.server.value})

        # extract name
        if (
            soup.title is not None
            and soup.title.text is not None
            and (name_match := REGEX_NAME.match(soup.title.text)) is not None
        ):
            data.update(name=name_match.group(1))
        else:
            data.update(name=None)

        # extract numbers
        for tag in soup.find_all("span", "number-format"):
            try:
                key = tag.parent.find_previous_sibling().text.lower()
                data[key] = int(float(tag.text))
            except (AttributeError, ValueError):
                pass

        # extract rate
        for tag in soup.find_all("span", "sales-rate"):
            with contextlib.suppress(AttributeError, ValueError):
                data["rate"] = float(tag.text)

        # fix key
        data = self._fix_stack_price_key(data)

        # save cache
        if self.cache is not None:
            cache_stub = self._cache_sub(itemid)
            cache_stub.parent.mkdir(parents=True, exist_ok=True)
            cache_stub.with_suffix(".json").write_text(json.dumps(data, indent=2, sort_keys=True))

        return data

    # step 3.1.2
    @staticmethod
    def _fix_stack_price_key(data: dict[str, Any]) -> dict[str, Any]:
        """
        Fix dictionary key.
        """
        new_key = r"stack price"

        for key in list(data.keys()):
            if "stack" in key.lower():
                data[new_key] = data[key]

        return data


def augment_item_info(item_info: dict[str, Any], **kwargs: Any) -> dict:
    """
    Extract item data from scrubbed info.
    """
    # singles
    try:
        price_single, sell_single = item_info["median"], True

        # do not sell items without a price
        if price_single <= 0:
            price_single, sell_single = 0, False

    except KeyError:
        price_single, sell_single = 0, False

    # stacks
    try:
        price_stacks, sell_stacks = item_info["stack price"], True

        # do not sell items without a price
        if price_stacks <= 0:
            price_stacks, sell_stacks = 0, False

    except KeyError:
        price_stacks, sell_stacks = 0, False

    # the name doesn't really matter
    try:
        name = item_info["name"]
    except KeyError:
        name = None

    result = {
        "name": name,
        "price_single": price_single,
        "stock_single": 5,
        "sell_single": sell_single,
        "buy_single": True,
        "rate_single": 1.0,
        "price_stacks": price_stacks,
        "stock_stacks": 5,
        "sell_stacks": sell_stacks,
        "buy_stacks": True,
        "rate_stacks": 1.0,
    }
    result.update(**kwargs)

    return result
