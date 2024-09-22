from ffxiahbot.auction.worker import Worker
from ffxiahbot.database import Database


def test_create_worker(populated_fake_db: Database) -> None:
    worker = Worker(populated_fake_db, rollback=True, fail=True)
    assert worker.fail is True
    assert worker.rollback is True
    assert worker.db is populated_fake_db

    with worker.scoped_session():
        pass
