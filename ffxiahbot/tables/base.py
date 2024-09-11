from collections.abc import Callable
from typing import Any

from sqlalchemy import DDLElement
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


@compiles(TINYINT, "sqlite")
def compile_tinyint(element: DDLElement, compiler: Callable[[Any], str], **kwargs: Any) -> str:
    """
    Compile TINYINT for SQLite test database.
    """
    return "INTEGER"
