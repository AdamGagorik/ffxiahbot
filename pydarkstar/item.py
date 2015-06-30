from .darkobject import DarkObject
import collections

fmt = collections.OrderedDict()
fmt['itemid'] = '{:>8}'
fmt['name'] = '{:>24}'
fmt['sell01'] = '{:>6}'
fmt['buy01'] = '{:>6}'
fmt['price01'] = '{:>16}'
fmt['stock01'] = '{:>7}'
fmt['rate01'] = '{:>7}'
fmt['sell12'] = '{:>6}'
fmt['buy12'] = '{:>6}'
fmt['price12'] = '{:>16}'
fmt['stock12'] = '{:>7}'
fmt['rate12'] = '{:>7}'


def title_str():
    objs = []
    for key in fmt.keys():
        objs.append(fmt[key].format(key))

    return ', '.join(objs) + '\n'


def value_str(item):
    objs = []
    for key in fmt.keys():
        value = getattr(item, key, None)
        objs.append(fmt[key].format(value))

    return ', '.join(objs) + '\n'


_template = \
    """
[Item]
    addr        = {addr}
    itemid      = {self.itemid}
    name        = {self.name}
    sell01      = {self.sell01}
    buy01       = {self.buy01}
    price01     = {self.price01}
    stock01     = {self.stock01}
    rate01      = {self.rate01}
    sell12      = {self.sell12}
    buy12       = {self.buy12}
    price12     = {self.price12}
    stock12     = {self.stock12}
    rate12      = {self.rate12}
"""[:-1]


class Item(DarkObject):
    """
    Item properties.

    :param itemid: unique item id
    :param name: item name

    :param sell01: sell single
    :param buy01: buy single
    :param price01: price (>= 1) for single
    :param stock01: restock count (>= 0) for single

    :param sell12: sell stack
    :param buy12: buy stack
    :param price12: price (>= 1) for stack
    :param stock12: restock count (>= 0) for stack
    """

    keys = ['itemid', 'name',
            'sell01', 'buy01', 'price01', 'stock01', 'rate01',
            'sell12', 'buy12', 'price12', 'stock12', 'rate12']

    @property
    def values(self):
        return [self.itemid, self.name,
                self.sell01, self.buy01, self.price01, self.stock01, self.rate01,
                self.sell12, self.buy12, self.price12, self.stock12, self.rate12]

    def __init__(self, itemid, name=None,
                 sell01=None, buy01=None, price01=None, stock01=None, rate01=None,
                 sell12=None, buy12=None, price12=None, stock12=None, rate12=None):
        super(Item, self).__init__()

        self._itemid = int(itemid)
        self._name = None

        self._sell01 = None
        self._sell12 = None

        self._buy01 = None
        self._buy12 = None

        self._price01 = None
        self._price12 = None

        self._stock01 = None
        self._stock12 = None

        self._rate01 = None
        self._rate12 = None

        self.name = name

        self.sell01 = sell01
        self.buy01 = buy01
        self.price01 = price01
        self.stock01 = stock01
        self.rate01 = rate01

        self.sell12 = sell12
        self.buy12 = buy12
        self.price12 = price12
        self.stock12 = stock12
        self.rate12 = rate12

        if not self._itemid >= 0:
            raise ValueError('itemid must be positive: %d' % self._itemid)

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
            value = '?'
        self._name = str(value)

    @property
    def sell01(self):
        return self._sell01

    @sell01.setter
    def sell01(self, value):
        if value is None:
            value = True
        self._sell01 = bool(value)

    @property
    def buy01(self):
        return self._buy01

    @buy01.setter
    def buy01(self, value):
        if value is None:
            value = True
        self._buy01 = bool(value)

    @property
    def price01(self):
        return self._price01

    @price01.setter
    def price01(self, value):
        if value is None:
            value = 1
        self._price01 = int(value)
        if self._price01 < 1:
            raise ValueError('price01 must be positive definite: %d' % self._price01)

    @property
    def stock01(self):
        return self._stock01

    @stock01.setter
    def stock01(self, value):
        if value is None:
            value = 0
        self._stock01 = int(value)
        if self._stock01 < 0:
            raise ValueError('stock01 must be positive: %d' % self._stock01)

    @property
    def rate01(self):
        return self._rate01

    @rate01.setter
    def rate01(self, value):
        if value is None:
            value = 1.0
        self._rate01 = float(value)
        if self._rate01 < 0.0 or self._rate01 > 1.0:
            raise ValueError('rate01 must be between 0 and 1: %d' % self._rate01)

    @property
    def sell12(self):
        return self._sell12

    @sell12.setter
    def sell12(self, value):
        if value is None:
            value = True
        self._sell12 = bool(value)

    @property
    def buy12(self):
        return self._buy12

    @buy12.setter
    def buy12(self, value):
        if value is None:
            value = True
        self._buy12 = bool(value)

    @property
    def price12(self):
        return self._price12

    @price12.setter
    def price12(self, value):
        if value is None:
            value = 1
        self._price12 = int(value)
        if self._price12 < 1:
            raise ValueError('price12 must be positive definite: %d' % self._price12)

    @property
    def stock12(self):
        return self._stock12

    @stock12.setter
    def stock12(self, value):
        if value is None:
            value = 0
        self._stock12 = int(value)
        if self._stock12 < 0:
            raise ValueError('stock12 must be positive: %d' % self._stock12)

    @property
    def rate12(self):
        return self._rate12

    @rate12.setter
    def rate12(self, value):
        if value is None:
            value = 1.0
        self._rate12 = float(value)
        if self._rate12 < 0.0 or self._rate12 > 1.0:
            raise ValueError('rate12 must be between 0 and 1: %d' % self._rate12)


if __name__ == '__main__':
    pass
