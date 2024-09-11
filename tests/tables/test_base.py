from sqlalchemy import inspect
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from ffxiahbot.database import Database
from ffxiahbot.tables.base import Base


def test_compile_tinyint(fake_db: Database) -> None:
    assert Base is not None

    class CustomBase(DeclarativeBase):
        pass

    class CustomTable(CustomBase):
        __tablename__ = "custom_table"

        id: Mapped[int] = mapped_column(
            TINYINT(10, unsigned=True), nullable=False, autoincrement=True, primary_key=True
        )

    CustomBase.metadata.create_all(fake_db.engine)
    assert set(inspect(fake_db.engine).get_table_names()) == {"custom_table"}
