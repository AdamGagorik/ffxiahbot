import logging
import os
import random
from pathlib import Path

import pandas as pd
import pytest

from ffxiahbot.database import Database
from ffxiahbot.tables.auctionhouse import AuctionHouse
from ffxiahbot.tables.base import Base


@pytest.fixture(scope="function")
def db_path() -> Path:
    return Path(__file__).parent.joinpath("test.db")


@pytest.fixture(scope="function")
def fake_db(db_path: Path) -> Database:
    assert AuctionHouse is not None
    logging.getLogger("sqlalchemy.pool").setLevel(logging.DEBUG)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    yield Database.sqlite(database=str(db_path))
    db_path.unlink(missing_ok=True)


@pytest.fixture(scope="function")
def populated_fake_db(fake_db: Database) -> Database:
    Base.metadata.create_all(fake_db.engine)
    return fake_db


@pytest.fixture(scope="function")
def real_db() -> Database:
    return Database.pymysql(
        hostname=os.environ.get("FFXIAHBOT_TEST_REAL_DB_HOSTNAME", "127.0.0.1"),
        database=os.environ.get("FFXIAHBOT_TEST_REAL_DB_DATABASE", "xidb"),
        username=os.environ.get("FFXIAHBOT_TEST_REAL_DB_USERNAME", "xi"),
        password=os.environ.get("FFXIAHBOT_TEST_REAL_DB_PASSWORD", "password"),
        port=3306,
    )


@pytest.fixture(scope="session", autouse=True)
def set_random_seed():
    random.seed(12345)


@pytest.fixture(scope="session", autouse=True)
def set_pandas_options():
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)
