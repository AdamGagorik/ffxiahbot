import collections

from ffxiahbot.darkobject import DarkObject

fmt = collections.OrderedDict()
fmt["itemid"] = "{:>8}"
fmt["name"] = "{:>24}"
fmt["sell_single"] = "{:>6}"
fmt["buy_single"] = "{:>6}"
fmt["price_single"] = "{:>16}"
fmt["stock_single"] = "{:>7}"
fmt["rate_single"] = "{:>7}"
fmt["sell_stacks"] = "{:>6}"
fmt["buy_stacks"] = "{:>6}"
fmt["price_stacks"] = "{:>16}"
fmt["stock_stacks"] = "{:>7}"
fmt["rate_stacks"] = "{:>7}"


def title_str():
    objs = []
    for key in fmt:
        objs.append(fmt[key].format(key))

    return ", ".join(objs) + "\n"


def value_str(item):
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


class Item(DarkObject):
    """
    Item properties.

    :param itemid: unique item id
    :param name: item name

    :param sell_single: sell single
    :param buy_single: buy single
    :param price_single: price (>= 1) for single
    :param stock_single: restock count (>= 0) for single

    :param sell_stacks: sell stack
    :param buy_stacks: buy stack
    :param price_stacks: price (>= 1) for stack
    :param stock_stacks: restock count (>= 0) for stack
    """

    keys = (
        "itemid",
        "name",
        "sell_single",
        "buy_single",
        "price_single",
        "stock_single",
        "rate_single",
        "sell_stacks",
        "buy_stacks",
        "price_stacks",
        "stock_stacks",
        "rate_stacks",
    )

    @property
    def values(self):
        return [
            self.itemid,
            self.name,
            self.sell_single,
            self.buy_single,
            self.price_single,
            self.stock_single,
            self.rate_single,
            self.sell_stacks,
            self.buy_stacks,
            self.price_stacks,
            self.stock_stacks,
            self.rate_stacks,
        ]

    def __init__(
        self,
        itemid,
        name=None,
        sell_single=None,
        buy_single=None,
        price_single=None,
        stock_single=None,
        rate_single=None,
        sell_stacks=None,
        buy_stacks=None,
        price_stacks=None,
        stock_stacks=None,
        rate_stacks=None,
    ):
        super().__init__()

        self._itemid = int(itemid)
        self._name = None

        self._sell_single = None
        self._sell_stacks = None

        self._buy_single = None
        self._buy_stacks = None

        self._price_single = None
        self._price_stacks = None

        self._stock_single = None
        self._stock_stacks = None

        self._rate_single = None
        self._rate_stacks = None

        self.name = name

        self.sell_single = sell_single
        self.buy_single = buy_single
        self.price_single = price_single
        self.stock_single = stock_single
        self.rate_single = rate_single

        self.sell_stacks = sell_stacks
        self.buy_stacks = buy_stacks
        self.price_stacks = price_stacks
        self.stock_stacks = stock_stacks
        self.rate_stacks = rate_stacks

        if not self._itemid >= 0:
            raise ValueError("itemid must be positive: %d" % self._itemid)

    def _init_notify(self):
        pass

    def __str__(self):
        return _template.format(self=self, addr=hex(id(self)))

    @property
    def itemid(self):
        return self._itemid

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value is None:
            value = "?"
        self._name = str(value)

    @property
    def sell_single(self):
        return self._sell_single

    @sell_single.setter
    def sell_single(self, value):
        if value is None:
            value = True
        self._sell_single = bool(value)

    @property
    def buy_single(self):
        return self._buy_single

    @buy_single.setter
    def buy_single(self, value):
        if value is None:
            value = True
        self._buy_single = bool(value)

    @property
    def price_single(self):
        return self._price_single

    @price_single.setter
    def price_single(self, value):
        if value is None:
            value = 1
        self._price_single = int(value)
        if self._price_single < 1:
            raise ValueError("price_single must be positive definite: %d" % self._price_single)

    @property
    def stock_single(self):
        return self._stock_single

    @stock_single.setter
    def stock_single(self, value):
        if value is None:
            value = 0
        self._stock_single = int(value)
        if self._stock_single < 0:
            raise ValueError("stock_single must be positive: %d" % self._stock_single)

    @property
    def rate_single(self):
        return self._rate_single

    @rate_single.setter
    def rate_single(self, value):
        if value is None:
            value = 1.0
        self._rate_single = float(value)
        if self._rate_single < 0.0 or self._rate_single > 1.0:
            raise ValueError("rate_single must be between 0 and 1: %d" % self._rate_single)

    @property
    def sell_stacks(self):
        return self._sell_stacks

    @sell_stacks.setter
    def sell_stacks(self, value):
        if value is None:
            value = True
        self._sell_stacks = bool(value)

    @property
    def buy_stacks(self):
        return self._buy_stacks

    @buy_stacks.setter
    def buy_stacks(self, value):
        if value is None:
            value = True
        self._buy_stacks = bool(value)

    @property
    def price_stacks(self):
        return self._price_stacks

    @price_stacks.setter
    def price_stacks(self, value):
        if value is None:
            value = 1
        self._price_stacks = int(value)
        if self._price_stacks < 1:
            raise ValueError("price_stacks must be positive definite: %d" % self._price_stacks)

    @property
    def stock_stacks(self):
        return self._stock_stacks

    @stock_stacks.setter
    def stock_stacks(self, value):
        if value is None:
            value = 0
        self._stock_stacks = int(value)
        if self._stock_stacks < 0:
            raise ValueError("stock_stacks must be positive: %d" % self._stock_stacks)

    @property
    def rate_stacks(self):
        return self._rate_stacks

    @rate_stacks.setter
    def rate_stacks(self, value):
        if value is None:
            value = 1.0
        self._rate_stacks = float(value)
        if self._rate_stacks < 0.0 or self._rate_stacks > 1.0:
            raise ValueError("rate_stacks must be between 0 and 1: %d" % self._rate_stacks)


if __name__ == "__main__":
    pass
