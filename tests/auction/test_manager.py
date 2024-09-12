from ffxiahbot.auction.manager import Manager
from ffxiahbot.database import Database


def test_buy_items(populated_fake_db: Database) -> None:
    manager = Manager.from_db(populated_fake_db, name="X", rollback=True, fail=True)
    assert manager is not None
    raise NotImplementedError


def test_restock_items(populated_fake_db: Database) -> None:
    manager = Manager.from_db(populated_fake_db, name="X", rollback=True, fail=True)
    assert manager is not None
    raise NotImplementedError
