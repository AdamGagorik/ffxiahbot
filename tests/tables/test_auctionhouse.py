from __future__ import annotations

from ffxiahbot.database import Database
from ffxiahbot.tables.auctionhouse import AuctionHouse
from tests.cookbook import AuctionHouseRowBuilder


def test_create_ah_row(populated_fake_db: Database) -> None:
    # check that the table is empty
    with populated_fake_db.scoped_session() as session:
        assert session.query(AuctionHouse).count() == 0

    # add a row to the table
    random_items = [AuctionHouseRowBuilder() for _ in range(10)]
    for item in random_items:
        item.add_item_for_sale(populated_fake_db)

    # check that a single row now exists with the expected values
    with populated_fake_db.scoped_session() as session:
        assert session.query(AuctionHouse).count() == len(random_items)
        for i, random_item in enumerate(random_items):
            random_item.validate_query_result(session.query(AuctionHouse).get(i + 1))

    # clear the table
    with populated_fake_db.scoped_session() as session:
        session.query(AuctionHouse).delete()

    # check that the table is empty
    with populated_fake_db.scoped_session() as session:
        assert session.query(AuctionHouse).count() == 0
