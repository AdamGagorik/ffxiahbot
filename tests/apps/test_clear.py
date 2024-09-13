from pathlib import Path

import pytest
from pytest import MonkeyPatch

import ffxiahbot.apps.clear
from ffxiahbot.auction.manager import Manager
from ffxiahbot.config import Config
from ffxiahbot.database import Database
from ffxiahbot.tables.auctionhouse import AuctionHouse
from tests.cookbook import RANDOMIZE as R
from tests.cookbook import AuctionHouseRowBuilder as AHR
from tests.cookbook import setup_ah_transactions


@pytest.fixture
def config() -> Config:
    return Config(name="A")


@pytest.fixture
def manager(populated_fake_db: Database) -> Manager:
    return Manager.from_db(populated_fake_db, name="A")


@pytest.fixture()
def transactions() -> tuple[AHR, ...]:
    return (
        *AHR.many(count=1, price=1, seller=0, seller_name="A", itemid=1, stack=1, buyer_name="X", sell_date=R, sale=R),
        *AHR.many(count=1, price=1, seller=2, seller_name="B", itemid=2, stack=1, buyer_name="X", sell_date=R, sale=R),
        *AHR.many(count=1, price=1, seller=0, seller_name="A", itemid=3, stack=1),
        *AHR.many(count=1, price=1, seller=2, seller_name="B", itemid=4, stack=1),
    )


@pytest.mark.parametrize("clear_all", [True, False])
def test_main(
    populated_fake_db: Database,
    config: Config,
    manager: Manager,
    transactions: tuple[AHR, ...],
    clear_all: bool,
    monkeypatch: MonkeyPatch,
) -> None:
    setup_ah_transactions(populated_fake_db, *transactions)

    with monkeypatch.context() as m:
        m.setattr(Config, "from_yaml", lambda *a, **kw: config)
        m.setattr(Manager, "create_database_and_manager", lambda *a, **kw: manager)

        # ensure database has rows
        with populated_fake_db.scoped_session() as session:
            assert session.query(AuctionHouse).count() == len(transactions)

        ffxiahbot.apps.clear.main(cfg_path=Path("config.yaml"), no_prompt=True, clear_all=clear_all)

        # ensure database was cleared
        with populated_fake_db.scoped_session() as session:
            if clear_all:
                assert session.query(AuctionHouse).count() == 0
            else:
                assert session.query(AuctionHouse).count() == sum(1 for t in transactions if t.seller != 0)
