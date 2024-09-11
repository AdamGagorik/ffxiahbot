"""
TestCase for SQL.
"""

import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError

from ffxiahbot.database import Database

EXPECTED_TABLE_NAMES: set[str] = {"auction_house", "delivery_box"}


def test_real_connection(real_db: Database):
    try:
        assert set(inspect(real_db.engine).get_table_names()) == EXPECTED_TABLE_NAMES
    except OperationalError:
        pytest.xfail("OperationalError")


def test_fake_connection(fake_db: Database):
    assert not inspect(fake_db.engine).get_table_names()


def test_populated_fake_db(populated_fake_db: Database):
    assert set(inspect(populated_fake_db.engine).get_table_names()) == EXPECTED_TABLE_NAMES
