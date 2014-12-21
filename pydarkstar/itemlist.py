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

    def set(self, *itemids, **kwargs):
        for itemid in itemids:
            i = self[itemid]
            for k in kwargs:
                if hasattr(i, k):
                    setattr(i, k, kwargs[k])
                else:
                    raise KeyError('%s' % str(k))

    def get(self, itemid):
        return self.items[itemid]

    def __getitem__(self, itemid):
        return self.items[itemid]

    def __len__(self):
        return len(self.items)

    def loadcsv(self, fname):
        pass

    def savecsv(self, fname):
        with open(fname, 'wb') as handle:
            handle.write('{}\n'.format(','.join(pydarkstar.item.Item.keys)))
            for i in self.items:
                handle.write('{}\n'.format(self.items[i]))

if __name__ == '__main__':
    pass
