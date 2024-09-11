from datetime import UTC, datetime

import pytest
from sqlalchemy.orm import Session

from ffxiahbot.auction.buyer import Buyer
from ffxiahbot.database import Database
from ffxiahbot.tables.auctionhouse import AuctionHouse
from ffxiahbot.timeutils import datetime_to_timestamp
from tests.cookbook import RANDOMIZE as R
from tests.cookbook import AuctionHouseRowBuilder as AHR
from tests.cookbook import setup_ah_transactions


@pytest.fixture()
def buy_date() -> datetime:
    return datetime(2000, 1, 1, tzinfo=UTC)


@pytest.fixture()
def buy_timestamp(buy_date: datetime) -> int:
    return datetime_to_timestamp(buy_date)


@pytest.fixture()
def transactions() -> tuple[AHR, ...]:
    return (
        *AHR.many(count=1, price=1, seller=1, seller_name="A", itemid=1, stack=1, buyer_name="W", sell_date=R, sale=R),
        *AHR.many(count=1, price=1, seller=2, seller_name="B", itemid=2, stack=1, buyer_name="X", sell_date=R, sale=R),
        *AHR.many(count=1, price=1, seller=3, seller_name="C", itemid=3, stack=0, buyer_name="Y", sell_date=R, sale=R),
        *AHR.many(count=1, price=1, seller=4, seller_name="D", itemid=4, stack=0, buyer_name="Z", sell_date=R, sale=R),
        *AHR.many(count=1, price=1, seller=5, seller_name="E", itemid=5, stack=1),
        *AHR.many(count=1, price=1, seller=6, seller_name="F", itemid=6, stack=1),
        *AHR.many(count=1, price=1, seller=7, seller_name="G", itemid=7, stack=0),
        *AHR.many(count=1, price=1, seller=8, seller_name="H", itemid=8, stack=0),
    )


def get_row_for_sale_by(session: Session, seller_name: str) -> AuctionHouse:
    return session.query(AuctionHouse).filter(AuctionHouse.seller_name == seller_name).first()


def test_buyer_buys_row(
    populated_fake_db: Database,
    transactions: tuple[AHR, ...],
    buy_date: datetime,
    buy_timestamp: int,
    seller_name: str = "E",
    buyer_name: str = "X",
    buy_price: int = 1,
) -> None:
    expected_transaction_table = setup_ah_transactions(populated_fake_db, *transactions)

    buyer = Buyer(populated_fake_db, buyer_name=buyer_name, fail=True)
    with populated_fake_db.scoped_session() as session:
        row = get_row_for_sale_by(session, seller_name)
        buyer.set_row_buyer_info(row, 0, buy_price)

    with populated_fake_db.scoped_session() as session:
        for _, expected_transaction in expected_transaction_table.iterrows():
            if expected_transaction.seller_name != seller_name:
                row = get_row_for_sale_by(session, expected_transaction.seller_name)
            else:
                row = get_row_for_sale_by(session, seller_name)
                expected_transaction.builder.sale = buy_price
                expected_transaction.builder.buyer_name = buyer_name
                expected_transaction.builder.validate_query_result(row)

            expected_transaction.builder.validate_query_result(row)


def test_buyer_raises_on_invalid_item(
    populated_fake_db: Database,
    transactions: tuple[AHR, ...],
    buy_date: datetime,
    buy_timestamp: int,
    seller_name: str = "A",
    buyer_name: str = "X",
    buy_price: int = 1,
):
    setup_ah_transactions(populated_fake_db, *transactions)
    buyer = Buyer(populated_fake_db, buyer_name=buyer_name, fail=True)
    with populated_fake_db.scoped_session() as session:
        row = get_row_for_sale_by(session, seller_name)
        with pytest.raises(RuntimeError):
            buyer.set_row_buyer_info(row, buy_timestamp, buy_price)
