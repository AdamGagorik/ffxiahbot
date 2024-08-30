from __future__ import annotations

import contextlib
import re
from collections.abc import Generator, Iterable
from dataclasses import dataclass
from typing import Any

from ffxiahbot.logutils import logger
from ffxiahbot.scrubbing.enums import ServerID
from ffxiahbot.scrubbing.scrubber import Scrubber

REGEX_CATEGORY: re.Pattern = re.compile(r"/browse/(\d+)/?.*")
REGEX_ITEM: re.Pattern = re.compile(r"/item/(\d+)")
REGEX_NAME: re.Pattern = re.compile(r"(.*?)\s*-?\s*(FFXIAH)?\.(com)?")


@dataclass()
class FFXIAHScrubber(Scrubber):
    """
    Get item data from the ffxiah.com website.
    """

    #: The FFXI server
    server: ServerID = ServerID.BAHAMUT
    #: number of threads to use
    num_threads: int | None = None

    def scrub(self, cat_urls: Iterable[str] | None = None, item_ids: Iterable[int] | None = None):
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
        if not item_ids:
            if not cat_urls:
                cat_urls = sorted(self._get_category_urls(), key=lambda x: list(map(float, re.findall(r"\d+", x))))

            logger.debug("# urls = %d", len(cat_urls))
            item_ids = sorted(set(self._get_itemids(cat_urls)))
        else:
            logger.debug("using passed ids")
            item_ids = sorted(set(item_ids))

            if cat_urls:
                logger.warning("passed urls ignored")

        failed, data = self._get_item_data(item_ids)
        logger.debug("item count = %d", len(item_ids))
        logger.debug("data count = %d", len(data))

        return failed, data

    # step 1
    def _get_category_urls(self) -> Generator[str]:
        """
        Parse http://www.ffxiah.com/browse to get URLs of the form http://www.ffxiah.com/{CategoryNumber}.
        """
        logger.debug("getting category urls")

        # the browse section of FFXIAH has a list of urls with category numbers
        path = "http://www.ffxiah.com/browse"
        logger.debug("open %s", path)
        soup = self.soup(path)
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

    # step 2
    def _get_itemids(self, urls: list[str]) -> Generator[int]:
        """
        Scrub urls of the form http://www.ffxiah.com/{CategoryNumber} for itemids.
        """
        logger.info("getting itemids")
        for i, url in enumerate(urls):
            logger.info("category %02d/%02d : %s", i + 1, len(urls), url)
            yield from self._get_itemids_for_category_url(url)

    # step 2.1
    def _get_itemids_for_category_url(self, url: str) -> Generator[int]:
        """
        Scrub url of the form http://www.ffxiah.com/{CategoryNumber} for itemids.
        """
        # create tag soup
        soup = self.soup(url)

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
        trs = tbody.find_all("tr")
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
                    try:
                        item = int(REGEX_ITEM.match(href).group(1))
                        count += 1
                        yield item

                    except (ValueError, IndexError):
                        logger.exception("failed to extract itemid!\n\n\trow %d of %s\n\n%s\n\n", j, url, row)
                else:
                    logger.error("failed to extract href!\n\n\trow %d of %s\n\n%s\n\n", j, url, row)
            else:
                logger.error("failed to extract 'a' tag!\n\n\trow %d of %s\n\n%s\n\n", j, url, row)

        # make sure we found something
        if not count:
            logger.error("could not find any itemids!")

    # step 3
    def _get_item_data(self, itemids: list[int]) -> tuple[dict[int, Exception], dict[int, dict[str, Any]]]:
        """
        Get metadata for many items.
        """
        logger.info("getting data")

        data = {}
        failed = {}

        # get data from itemids
        for i, itemid in enumerate(itemids):
            try:
                result = self._get_item_data_for_itemid(itemid, index=i, total=len(itemids))
                data[itemid] = result
            except Exception as e:
                logger.exception("failed to scrub %d!", itemid)
                failed[itemid] = e

        if failed:
            for itemid in failed:
                logger.error("failed to scrub %d!", itemid)

        return failed, data

    # step 3.1
    def _get_item_data_for_itemid(self, itemid: int, index: int = 0, total: int = 0) -> dict[str, Any]:
        """
        Get metadata for single item.
        """
        percent = float(index) / float(total) * 100.0 if total > 0 else 0.0

        data = {"name": None, "itemid": itemid}
        url = self._create_item_url(itemid)

        # create tag soup
        logger.debug("open server=%s (%06d/%06d,%6.2f) %s", self.server, index, total, percent, url)
        soup = self.soup(url, absolute=True, sid=self.server.value)

        # extract name
        try:
            data.update(name=REGEX_NAME.match(soup.title.text).group(1))
        except AttributeError:
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

        return data

    def _get_item_data_for_itemid_map(self, args):
        return self._get_item_data_for_itemid(*args)

    # step 3.1.1
    @staticmethod
    def _create_item_url(itemid: int) -> str:
        """
        Create URL from itemid.
        """
        return f"http://www.ffxiah.com/item/{itemid}"

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


def extract(data: dict[int, dict[str, Any]], itemid: int, **kwargs: Any):
    """
    Extract item data from scrubbed info.
    """
    # singles
    try:
        price_single, sell_single = data[itemid]["median"], True

        # do not sell items without a price
        if price_single <= 0:
            price_single, sell_single = None, False

    except KeyError:
        price_single, sell_single = None, False

    # stacks
    try:
        price_stacks, sell_stacks = data[itemid]["stack price"], True

        # do not sell items without a price
        if price_stacks <= 0:
            price_stacks, sell_stacks = None, False

    except KeyError:
        price_stacks, sell_stacks = None, False

    # the name doesn't really matter
    try:
        name = data[itemid]["name"]
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
