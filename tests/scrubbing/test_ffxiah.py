import aiohttp
import pytest

from ffxiahbot.scrubbing.ffxiah import FFXIAHScrubber, augment_item_info


@pytest.mark.asyncio
async def test_get_category_urls():
    async with aiohttp.ClientSession() as session:
        await FFXIAHScrubber()._get_category_urls(session)


@pytest.mark.asyncio
async def test_get_itemids_for_category_url():
    url = r"http://www.ffxiah.com/browse/49/ninja-tools"
    async with aiohttp.ClientSession() as session:
        await FFXIAHScrubber()._get_itemids_for_category_url(session, url)


@pytest.mark.asyncio
async def test_get_itemids():
    urls = [
        r"http://www.ffxiah.com/browse/49/ninja-tools",
        r"http://www.ffxiah.com/browse/56/breads-rice",
    ]
    async with aiohttp.ClientSession() as session:
        await FFXIAHScrubber()._get_item_ids(session, urls)


@pytest.mark.asyncio
async def test_get_item_data_for_itemid():
    async with aiohttp.ClientSession() as session:
        await FFXIAHScrubber()._get_item_data_for_itemid(session, 4096)


@pytest.mark.asyncio
async def test_get_item_data():
    async with aiohttp.ClientSession() as session:
        await FFXIAHScrubber()._get_item_data(session, list(range(1, 9)))


@pytest.mark.asyncio
async def test_scrub():
    await FFXIAHScrubber().scrub(item_ids={1, 2, 3, 4})


@pytest.mark.asyncio
async def test_augment_item_info():
    async with aiohttp.ClientSession() as session:
        results, failed = await FFXIAHScrubber()._get_item_data(session, [4096])
        kwargs = augment_item_info(results[4096])
        assert kwargs["name"] == "Fire Crystal"
