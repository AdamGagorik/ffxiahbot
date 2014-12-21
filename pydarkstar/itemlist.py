"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import pydarkstar.darkobject
import pydarkstar.item
import collections

class ItemList(pydarkstar.darkobject.DarkObject):
    """
    Container for Item objects.
    """
    def __init__(self):
        super(ItemList, self).__init__()
        self.items = collections.OrderedDict()

    def add(self, itemid, *args, **kwargs):
        i = pydarkstar.item.Item(itemid, *args, **kwargs)
        if i.itemid in self.items:
            raise KeyError('duplicate item found: %d' % i.itemid)
        self.items[i.itemid] = i
        return i

if __name__ == '__main__':
    pass
