from datetime import UTC, datetime

import pytest
from sqlalchemy import Null

from ffxiahbot.auction.seller import Seller
from ffxiahbot.database import Database
from ffxiahbot.tables.auctionhouse import AuctionHouse
from ffxiahbot.timeutils import datetime_to_timestamp


@pytest.fixture()
def sell_date() -> datetime:
    return datetime(2000, 2, 2, tzinfo=UTC)


@pytest.fixture()
def sell_timestamp(sell_date: datetime) -> int:
    return datetime_to_timestamp(sell_date)


def test_set_history(populated_fake_db: Database, sell_timestamp) -> None:
    # ensure database has 0 rows
    with populated_fake_db.scoped_session() as session:
        assert session.query(AuctionHouse).count() == 0

    # set history for item
    seller = Seller(populated_fake_db, seller=1, seller_name="X", fail=True)
    seller.set_history(itemid=1, stack=False, price=1024, date=sell_timestamp, count=10)

    # ensure database has 10 rows
    with populated_fake_db.scoped_session() as session:
        assert session.query(AuctionHouse).count() == 10
        assert session.query(AuctionHouse).filter(AuctionHouse.itemid == 1).count() == 10
        assert session.query(AuctionHouse).filter(AuctionHouse.stack == 1).count() == 0
        assert session.query(AuctionHouse).filter(AuctionHouse.stack == 0).count() == 10
        assert session.query(AuctionHouse).filter(AuctionHouse.seller == 1).count() == 10
        assert session.query(AuctionHouse).filter(AuctionHouse.seller_name == "X").count() == 10
        assert session.query(AuctionHouse).filter(AuctionHouse.date == sell_timestamp).count() == 10
        assert session.query(AuctionHouse).filter(AuctionHouse.price == 1024).count() == 10
        assert session.query(AuctionHouse).filter(AuctionHouse.buyer_name == "X").count() == 10
        assert session.query(AuctionHouse).filter(AuctionHouse.sale == 1024).count() == 10
        assert session.query(AuctionHouse).filter(AuctionHouse.sell_date == sell_timestamp).count() == 10


def test_sell_item(populated_fake_db: Database, sell_timestamp) -> None:
    # ensure database has 0 rows
    with populated_fake_db.scoped_session() as session:
        assert session.query(AuctionHouse).count() == 0

    # sell item
    seller = Seller(populated_fake_db, seller=1, seller_name="X", fail=True)
    seller.sell_item(itemid=1, stack=True, date=sell_timestamp, price=1024, count=5)

    # ensure database has 5 rows
    with populated_fake_db.scoped_session() as session:
        assert session.query(AuctionHouse).count() == 5
        assert session.query(AuctionHouse).filter(AuctionHouse.itemid == 1).count() == 5
        assert session.query(AuctionHouse).filter(AuctionHouse.stack == 1).count() == 5
        assert session.query(AuctionHouse).filter(AuctionHouse.stack == 0).count() == 0
        assert session.query(AuctionHouse).filter(AuctionHouse.seller == 1).count() == 5
        assert session.query(AuctionHouse).filter(AuctionHouse.seller_name == "X").count() == 5
        assert session.query(AuctionHouse).filter(AuctionHouse.date == sell_timestamp).count() == 5
        assert session.query(AuctionHouse).filter(AuctionHouse.price == 1024).count() == 5
        assert session.query(AuctionHouse).filter(AuctionHouse.buyer_name == Null).count() == 5
        assert session.query(AuctionHouse).filter(AuctionHouse.sale == 0).count() == 5
        assert session.query(AuctionHouse).filter(AuctionHouse.sell_date == Null).count() == 5
