from pathlib import Path

import pytest
from pytest import MonkeyPatch

import ffxiahbot.apps.refill
from ffxiahbot.auction.manager import Manager
from ffxiahbot.config import Config
from ffxiahbot.database import Database
from ffxiahbot.item import Item
from ffxiahbot.itemlist import ItemList
from ffxiahbot.tables.auctionhouse import AuctionHouse


@pytest.fixture
def config() -> Config:
    return Config()


@pytest.fixture
def item_list() -> ItemList:
    return ItemList(
        items={
            1: Item(
                itemid=1,
                name="Fake Item A",
                sell_single=True,
                buy_single=True,
                price_single=100,
                stock_single=6,
                rate_single=1.0,
                sell_stacks=True,
                buy_stacks=True,
                price_stacks=200,
                stock_stacks=8,
                rate_stacks=1.0,
            ),
        }
    )


@pytest.fixture
def manager(populated_fake_db: Database) -> Manager:
    return Manager.from_db(populated_fake_db, name="test")


def test_main(
    populated_fake_db: Database, config: Config, item_list: ItemList, manager: Manager, monkeypatch: MonkeyPatch
) -> None:
    with monkeypatch.context() as m:
        m.setattr(Config, "from_yaml", lambda *a, **kw: config)
        m.setattr(ItemList, "from_csv", lambda *a, **kw: item_list)
        m.setattr(Manager, "create_database_and_manager", lambda *a, **kw: manager)
        ffxiahbot.apps.refill.main(cfg_path=Path("config.yaml"), inp_csvs=[Path("items.csv")], no_prompt=True)

    # check that the items were restocked
    with populated_fake_db.scoped_session() as session:
        for itemid, item in item_list.items.items():
            assert (
                session.query(AuctionHouse)
                .filter(AuctionHouse.itemid == itemid, AuctionHouse.stack == 0, AuctionHouse.sale != 0)
                .count()
                == 1
            )
            assert (
                session.query(AuctionHouse)
                .filter(AuctionHouse.itemid == itemid, AuctionHouse.stack == 1, AuctionHouse.sale != 0)
                .count()
                == 1
            )
            assert (
                session.query(AuctionHouse)
                .filter(AuctionHouse.itemid == itemid, AuctionHouse.stack == 0, AuctionHouse.sale == 0)
                .count()
                == item.stock_single
            )
            assert (
                session.query(AuctionHouse)
                .filter(AuctionHouse.itemid == itemid, AuctionHouse.stack == 1, AuctionHouse.sale == 0)
                .count()
                == item.stock_stacks
            )
            assert (
                session.query(AuctionHouse)
                .filter(AuctionHouse.itemid == itemid, AuctionHouse.stack == 0, AuctionHouse.sale == 0)
                .first()
                .price
                == item.price_single
            )
            assert (
                session.query(AuctionHouse)
                .filter(AuctionHouse.itemid == itemid, AuctionHouse.stack == 1, AuctionHouse.sale == 0)
                .first()
                .price
                == item.price_stacks
            )
