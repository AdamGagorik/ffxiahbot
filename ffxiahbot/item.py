from __future__ import annotations

import collections

from pydantic import BaseModel, ConfigDict, Field

fmt = collections.OrderedDict()
fmt["itemid"] = "{:>8}"
fmt["name"] = "{:>24}"
fmt["sell_single"] = "{:>11}"
fmt["buy_single"] = "{:>11}"
fmt["price_single"] = "{:>16}"
fmt["stock_single"] = "{:>12}"
fmt["rate_single"] = "{:>12}"
fmt["sell_stacks"] = "{:>11}"
fmt["buy_stacks"] = "{:>11}"
fmt["price_stacks"] = "{:>16}"
fmt["stock_stacks"] = "{:>12}"
fmt["rate_stacks"] = "{:>12}"


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
    addr        = {addr}
    itemid      = {self.itemid}
    name        = {self.name}
    sell_single      = {self.sell_single}
    buy_single       = {self.buy_single}
    price_single     = {self.price_single}
    stock_single     = {self.stock_single}
    rate_single      = {self.rate_single}
    sell_stacks      = {self.sell_stacks}
    buy_stacks       = {self.buy_stacks}
    price_stacks     = {self.price_stacks}
    stock_stacks     = {self.stock_stacks}
    rate_stacks      = {self.rate_stacks}
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
        rate_single: sell rate (0.0 <= rate <= 1.0) for singles.
        rate_stacks: sell rate (0.0 <= rate <= 1.0) for stacks.
    """

    model_config = ConfigDict(extra="forbid")

    #: A unique item id.
    itemid: int = Field(ge=0)
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
    price_single: int = Field(default=1, gt=0)
    #: Price (>= 1) for stacks.
    price_stacks: int = Field(default=1, gt=0)
    #: Restock count (>= 0) for singles.
    stock_single: int = Field(default=0, ge=0)
    #: Restock count (>= 0) for stacks.
    stock_stacks: int = Field(default=0, ge=0)
    #: Sell rate (0.0 <= rate <= 1.0) for singles.
    rate_single: float = Field(default=1.0, ge=0.0, le=1.0)
    #: Sell rate (0.0 <= rate <= 1.0) for stacks.
    rate_stacks: float = Field(default=1.0, ge=0.0, le=1.0)

    def __str__(self) -> str:
        return _template.format(self=self, addr=hex(id(self)))
