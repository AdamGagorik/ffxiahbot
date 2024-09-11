import pytest

from ffxiahbot.auction.browser import Browser
from ffxiahbot.database import Database
from tests.cookbook import RANDOMIZE as R
from tests.cookbook import AuctionHouseRowBuilder as AHR
from tests.cookbook import setup_ah_transactions


def test_browser_count_empty(populated_fake_db: Database) -> None:
    browser = Browser(populated_fake_db, fail=True)
    assert browser.count() == 0


def test_browser_count_one_item(populated_fake_db: Database) -> None:
    browser = Browser(populated_fake_db, fail=True)
    AHR().add_item_for_sale(populated_fake_db)
    assert browser.count() == 1


@pytest.mark.parametrize(
    "transactions",
    [
        pytest.param(
            [
                *AHR.many(count=1, seller=1, seller_name="A", itemid=1, stack=1, buyer_name="B", sell_date=R, sale=R),
                *AHR.many(count=2, seller=1, seller_name="A", itemid=2, stack=1, buyer_name="B", sell_date=R, sale=R),
                *AHR.many(count=3, seller=1, seller_name="A", itemid=1, stack=0, buyer_name="B", sell_date=R, sale=R),
                *AHR.many(count=4, seller=1, seller_name="A", itemid=2, stack=0, buyer_name="B", sell_date=R, sale=R),
                *AHR.many(count=5, seller=1, seller_name="A", itemid=1, stack=1),
                *AHR.many(count=6, seller=1, seller_name="A", itemid=2, stack=1),
                *AHR.many(count=7, seller=1, seller_name="A", itemid=1, stack=0),
                *AHR.many(count=8, seller=1, seller_name="A", itemid=2, stack=0),
            ],
            id="one seller",
        ),
        pytest.param(
            [
                *AHR.many(count=1, seller=1, seller_name="A", itemid=1, stack=1, buyer_name="B", sell_date=R, sale=R),
                *AHR.many(count=2, seller=1, seller_name="A", itemid=2, stack=1, buyer_name="B", sell_date=R, sale=R),
                *AHR.many(count=3, seller=1, seller_name="A", itemid=1, stack=0, buyer_name="B", sell_date=R, sale=R),
                *AHR.many(count=4, seller=1, seller_name="A", itemid=2, stack=0, buyer_name="B", sell_date=R, sale=R),
                *AHR.many(count=5, seller=1, seller_name="A", itemid=1, stack=1),
                *AHR.many(count=6, seller=1, seller_name="A", itemid=2, stack=1),
                *AHR.many(count=7, seller=1, seller_name="A", itemid=1, stack=0),
                *AHR.many(count=8, seller=1, seller_name="A", itemid=2, stack=0),
                *AHR.many(count=8, seller=2, seller_name="B", itemid=1, stack=1, buyer_name="A", sell_date=R, sale=R),
                *AHR.many(count=7, seller=2, seller_name="B", itemid=2, stack=1, buyer_name="A", sell_date=R, sale=R),
                *AHR.many(count=6, seller=2, seller_name="B", itemid=1, stack=0, buyer_name="A", sell_date=R, sale=R),
                *AHR.many(count=5, seller=2, seller_name="B", itemid=2, stack=0, buyer_name="A", sell_date=R, sale=R),
                *AHR.many(count=4, seller=2, seller_name="B", itemid=1, stack=1),
                *AHR.many(count=3, seller=2, seller_name="B", itemid=2, stack=1),
                *AHR.many(count=2, seller=2, seller_name="B", itemid=1, stack=0),
                *AHR.many(count=1, seller=2, seller_name="B", itemid=2, stack=0),
            ],
            id="two sellers",
        ),
    ],
)
def test_browser_get_stock_and_price(populated_fake_db: Database, transactions: tuple[AHR]) -> None:
    builder = setup_ah_transactions(populated_fake_db, *transactions)
    browser = Browser(populated_fake_db, fail=True)

    # validate totals being sold
    for i in builder.itemid.unique():
        assert browser.get_stock(i, stack=True, seller=None) == len(
            builder.query(f"itemid == {i} & stack == 1 & sale.isnull()")
        )
        assert browser.get_stock(i, stack=False, seller=None) == len(
            builder.query(f"itemid == {i} & stack == 0 & sale.isnull()")
        )

    # validate totals being sold for seller
    for seller in builder.seller.unique():
        for i in builder.itemid.unique():
            assert browser.get_stock(i, stack=True, seller=seller) == len(
                builder.query(f"itemid == {i} & stack == 1 & sale.isnull() & seller == {seller}")
            )
            assert browser.get_stock(i, stack=False, seller=seller) == len(
                builder.query(f"itemid == {i} & stack == 0 & sale.isnull() & seller == {seller}")
            )

    # validate min price for item up for sale
    for i in builder.itemid.unique():
        assert (
            browser.get_price(i, stack=True, seller=None)
            == builder.query(f"itemid == {i} & stack == 1 & sale > 0").price.min()
        )
        assert (
            browser.get_price(i, stack=False, seller=None)
            == builder.query(f"itemid == {i} & stack == 0 & sale > 0").price.min()
        )

    # validate min price for item up for sale by seller
    for seller in builder.seller.unique():
        for i in builder.itemid.unique():
            assert (
                browser.get_price(i, stack=True, seller=seller)
                == builder.query(f"itemid == {i} & stack == 1 & sale > 0 & seller == {seller}").price.min()
            )
            assert (
                browser.get_price(i, stack=False, seller=seller)
                == builder.query(f"itemid == {i} & stack == 0 & sale > 0 & seller == {seller}").price.min()
            )
