import pytest

from ffxiahbot.auction.cleaner import Cleaner
from ffxiahbot.database import Database
from ffxiahbot.tables.auctionhouse import AuctionHouse
from tests.cookbook import RANDOMIZE as R
from tests.cookbook import AuctionHouseRowBuilder as AHR
from tests.cookbook import setup_ah_transactions


@pytest.fixture()
def transactions() -> tuple[AHR, ...]:
    return (
        *AHR.many(count=1, price=1, seller=1, seller_name="A", itemid=1, stack=1, buyer_name="X", sell_date=R, sale=R),
        *AHR.many(count=1, price=1, seller=2, seller_name="B", itemid=2, stack=1, buyer_name="X", sell_date=R, sale=R),
        *AHR.many(count=1, price=1, seller=1, seller_name="A", itemid=3, stack=1),
        *AHR.many(count=1, price=1, seller=2, seller_name="B", itemid=4, stack=1),
    )


def test_clear_all(populated_fake_db: Database, transactions: tuple[AHR, ...]) -> None:
    setup_ah_transactions(populated_fake_db, *transactions)
    # ensure database has 4 rows
    with populated_fake_db.scoped_session() as session:
        assert session.query(AuctionHouse).count() == 4

    # clear all rows
    cleaner = Cleaner(populated_fake_db, fail=True)
    cleaner.clear(seller=None)

    # ensure database has 0 rows
    with populated_fake_db.scoped_session() as session:
        assert session.query(AuctionHouse).count() == 0


def test_clear_for_seller(populated_fake_db: Database, transactions: tuple[AHR, ...]) -> None:
    setup_ah_transactions(populated_fake_db, *transactions)
    # ensure database has 4 rows
    with populated_fake_db.scoped_session() as session:
        assert session.query(AuctionHouse).count() == 4

    # clear rows for seller 1
    cleaner = Cleaner(populated_fake_db, fail=True)
    cleaner.clear(seller=1)

    # ensure database has 2 rows
    with populated_fake_db.scoped_session() as session:
        assert session.query(AuctionHouse).count() == 2
        assert session.query(AuctionHouse).filter(AuctionHouse.seller == 1).count() == 0
        assert session.query(AuctionHouse).filter(AuctionHouse.seller == 2).count() == 2
