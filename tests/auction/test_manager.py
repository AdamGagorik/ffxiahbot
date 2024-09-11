from ffxiahbot.auction.manager import Manager
from ffxiahbot.database import Database


def test_buy_items(populated_fake_db: Database) -> None:
    manager = Manager(populated_fake_db, seller_name="X", buyer_name="X", fail=True)
    assert manager is not None
    raise NotImplementedError


def test_restock_items(populated_fake_db: Database) -> None:
    manager = Manager(populated_fake_db, seller_name="X", buyer_name="X", fail=True)
    assert manager is not None
    raise NotImplementedError
