"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import pydarkstar.darkobject

class Item(pydarkstar.darkobject.DarkObject):
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
            'sell01', 'buy01', 'price01', 'stock01',
            'sell12', 'buy12', 'price12', 'stock12']

    @property
    def values(self):
        return [self.itemid, self.name,
                self.sell01, self.buy01, self.price01, self.stock01,
                self.sell12, self.buy12, self.price12, self.stock12]

    def __init__(self, itemid, name=None,
            sell01=None, buy01=None, price01=None, stock01=None,
            sell12=None, buy12=None, price12=None, stock12=None):
        super(Item, self).__init__()

        self._itemid   = int(itemid)
        self._name     = None

        self._sell01  = None
        self._sell12  = None

        self._price01  = None
        self._price12  = None

        self._stack01  = None
        self._stock12  = None

        self.name = name

        self.sell01 = sell01
        self.buy01 = buy01
        self.price01 = price01
        self.stock01 = stock01

        self.sell12 = sell12
        self.buy12 = buy12
        self.price12 = price12
        self.stock12 = stock12

        if not self._itemid >= 0:
            raise ValueError('itemid must be positive: %d' % self._itemid)

    def __str__(self):
        return ','.join(map(str, map(lambda x : getattr(self, x), self.keys)))

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

if __name__ == '__main__':
    pass
