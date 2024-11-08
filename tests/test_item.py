from typing import Any

import pytest

from ffxiahbot.item import Item


@pytest.mark.parametrize(
    "kwargs,error",
    [
        pytest.param({"itemid": 0, "name": "A"}, None, id="name=A"),
        pytest.param({"itemid": 0, "price_single": 1}, None, id="price_single=1"),
        pytest.param({"itemid": 0, "price_single": -1}, ValueError, id="price_single=-1 raises"),
        pytest.param({"itemid": 0, "price_stacks": 1}, None, id="price_stacks=1"),
        pytest.param({"itemid": 0, "price_stacks": -1}, ValueError, id="price_stacks=-1 raises"),
        pytest.param({"itemid": 0, "stock_single": 0}, None, id="stock_single=0"),
        pytest.param({"itemid": 0, "stock_single": -1}, ValueError, id="stock_single=-1"),
        pytest.param({"itemid": 0, "stock_stacks": 0}, None, id="stock_stacks=0"),
        pytest.param({"itemid": 0, "stock_stacks": -1}, ValueError, id="stock_stacks=-1"),
        pytest.param({"itemid": 0, "sell_rate_single": 0.0}, None, id="sell_rate_single=0.0"),
        pytest.param({"itemid": 0, "sell_rate_single": 0.5}, None, id="sell_rate_single=0.5"),
        pytest.param({"itemid": 0, "sell_rate_single": 1.0}, None, id="sell_rate_single=1.0"),
        pytest.param({"itemid": 0, "sell_rate_single": -1.5}, ValueError, id="sell_rate_single=-1.5"),
        pytest.param({"itemid": 0, "sell_rate_single": +1.5}, ValueError, id="sell_rate_single=+1.5"),
        pytest.param({"itemid": 0, "sell_rate_stacks": 0.0}, None, id="sell_rate_stacks=0.0"),
        pytest.param({"itemid": 0, "sell_rate_stacks": 0.5}, None, id="sell_rate_stacks=0.5"),
        pytest.param({"itemid": 0, "sell_rate_stacks": 1.0}, None, id="sell_rate_stacks=1.0"),
        pytest.param({"itemid": 0, "sell_rate_stacks": -1.5}, ValueError, id="sell_rate_stacks=-1.5"),
        pytest.param({"itemid": 0, "sell_rate_stacks": +1.5}, ValueError, id="sell_rate_stacks=+1.5"),
        pytest.param({"itemid": 0, "buy_rate_single": 0.0}, None, id="buy_rate_single=0.0"),
        pytest.param({"itemid": 0, "buy_rate_single": 0.5}, None, id="buy_rate_single=0.5"),
        pytest.param({"itemid": 0, "buy_rate_single": 1.0}, None, id="buy_rate_single=1.0"),
        pytest.param({"itemid": 0, "buy_rate_single": -1.5}, ValueError, id="buy_rate_single=-1.5"),
        pytest.param({"itemid": 0, "buy_rate_single": +1.5}, ValueError, id="buy_rate_single=+1.5"),
        pytest.param({"itemid": 0, "buy_rate_stacks": 0.0}, None, id="buy_rate_stacks=0.0"),
        pytest.param({"itemid": 0, "buy_rate_stacks": 0.5}, None, id="buy_rate_stacks=0.5"),
        pytest.param({"itemid": 0, "buy_rate_stacks": 1.0}, None, id="buy_rate_stacks=1.0"),
        pytest.param({"itemid": 0, "buy_rate_stacks": -1.5}, ValueError, id="buy_rate_stacks=-1.5"),
        pytest.param({"itemid": 0, "buy_rate_stacks": +1.5}, ValueError, id="buy_rate_stacks=+1.5"),
    ],
)
def test_create_item_raises(kwargs: dict[str, Any], error: type[Exception] | None):
    if error:
        with pytest.raises(error):
            Item(**kwargs)
    else:
        item = Item(**kwargs)
        for key, value in kwargs.items():
            assert getattr(item, key) == value
