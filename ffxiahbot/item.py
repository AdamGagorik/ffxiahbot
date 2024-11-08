from __future__ import annotations

import collections
import functools
from collections.abc import Generator

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

fmt = collections.OrderedDict()
fmt["itemid"] = "{:>8}"
fmt["name"] = "{:>24}"
fmt["sell_single"] = "{:>11}"
fmt["buy_single"] = "{:>11}"
fmt["price_single"] = "{:>16}"
fmt["stock_single"] = "{:>12}"
fmt["buy_rate_single"] = "{:>16}"
fmt["sell_rate_single"] = "{:>16}"
fmt["sell_stacks"] = "{:>11}"
fmt["buy_stacks"] = "{:>11}"
fmt["price_stacks"] = "{:>16}"
fmt["stock_stacks"] = "{:>12}"
fmt["buy_rate_stacks"] = "{:>16}"
fmt["sell_rate_stacks"] = "{:>16}"


def item_csv_title_str() -> str:
    objs = []
    for key in fmt:
        objs.append(fmt[key].format(key))

    return ", ".join(objs) + "\n"


def item_csv_value_str(item: Item) -> str:
    objs = []
    for key in fmt:
        value = getattr(item, key, None)
        objs.append(fmt[key].format(value))

    return ", ".join(objs) + "\n"


_template = """
[Item]
    id         = {self.itemid}
    addr       = {addr}
    name       = {self.name}

[Item.Single]
    buy        = {self.buy_single}
    sell       = {self.sell_single}
    price      = {self.price_single}
    stock      = {self.stock_single}
    buy_rate   = {self.buy_rate_single}
    sell_rate  = {self.sell_rate_single}

[Item.Stacks]
    buy        = {self.buy_stacks}
    sell       = {self.sell_stacks}
    price      = {self.price_stacks}
    stock      = {self.stock_stacks}
    buy_rate   = {self.buy_rate_stacks}
    sell_rate  = {self.sell_rate_stacks}
"""[:-1]


class Item(BaseModel):
    """
    Item properties.

    Args:
        itemid: A unique item id.
        name: The item's name.
        sell_single: sell singles?
        buy_single: buy singles?
        price_single: price (>= 1) for singles.
        stock_single: restock count (>= 0) for singles.
        sell_stacks: sell stacks?
        buy_stacks: buy stacks?
        price_stacks: price (>= 1) for stacks.
        stock_stacks: restock count (>= 0) for stacks.
        buy_rate_single: buy rate (0.0 <= rate <= 1.0) for singles.
        sell_rate_single: sell rate (0.0 <= rate <= 1.0) for singles.
        sell_rate_stacks: sell rate (0.0 <= rate <= 1.0) for stacks.
        buy_rate_stacks: buy rate (0.0 <= rate <= 1.0) for stacks.
    """

    model_config = ConfigDict(extra="forbid")

    #: A unique item id.
    itemid: int = Field(ge=0, validation_alias=AliasChoices("id", "itemid"))
    #: The item's name.
    name: str = "?"
    #: Sell singles?
    sell_single: bool = True
    #: Sell stacks?
    sell_stacks: bool = True
    #: Buy singles?
    buy_single: bool = True
    #: Buy stacks?
    buy_stacks: bool = True
    #: Price (>= 1) for singles.
    price_single: int = Field(default=1, ge=0)
    #: Price (>= 1) for stacks.
    price_stacks: int = Field(default=1, ge=0)
    #: Restock count (>= 0) for singles.
    stock_single: int = Field(default=0, ge=0)
    #: Restock count (>= 0) for stacks.
    stock_stacks: int = Field(default=0, ge=0)
    #: Buy rate (0.0 <= rate <= 1.0) for singles.
    buy_rate_single: float = Field(default=1.0, ge=0.0, le=1.0, validation_alias=AliasChoices("buy_rate_single"))
    #: Sell rate (0.0 <= rate <= 1.0) for singles.
    sell_rate_single: float = Field(
        default=1.0, ge=0.0, le=1.0, validation_alias=AliasChoices("sell_rate_single", "rate_single")
    )
    #: Buy rate (0.0 <= rate <= 1.0) for stacks.
    buy_rate_stacks: float = Field(default=1.0, ge=0.0, le=1.0, validation_alias=AliasChoices("buy_rate_stacks"))
    #: Sell rate (0.0 <= rate <= 1.0) for stacks.
    sell_rate_stacks: float = Field(
        default=1.0, ge=0.0, le=1.0, validation_alias=AliasChoices("sell_rate_stacks", "rate_stacks")
    )

    @classmethod
    def aliases(cls) -> Generator[str]:
        yield from cls.model_fields.keys()

    def __str__(self) -> str:
        return _template.format(self=self, addr=hex(id(self)))


@functools.lru_cache(maxsize=1)
def allowed_item_keys() -> set[str]:
    def _() -> Generator[str]:
        for key, field_info in Item.model_fields.items():
            yield key
            if hasattr(field_info, "validation_alias") and isinstance(field_info.validation_alias, AliasChoices):
                for alias in field_info.validation_alias.choices:
                    if isinstance(alias, str):
                        yield alias

    return set(_())
