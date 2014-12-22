"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import pydarkstar.darkobject
import pydarkstar.item
import collections
import re

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
        regex_C = re.compile(r'#.*$')

        regex_T = '[{0}{1}]?True[{0}{1}]?'.format('"', "'")
        regex_T = re.compile(regex_T, re.IGNORECASE)

        regex_F = '[{0}{1}]?False[{0}{1}]?'.format('"', "'")
        regex_F = re.compile(regex_F, re.IGNORECASE)

        with open(fname, 'rb') as handle:
            # first line is item titles
            line = handle.readline()

            # ignore comments
            line = regex_C.sub('', line).strip()

            # split into tokens
            keys = line.split(',')
            keys = map(lambda x : x.strip().lower(), keys)

            # make sure keys are valid
            for k in keys:
                if not k in pydarkstar.item.Item.keys:
                    raise RuntimeError('unknown column: %s' % k)

            # check for primary key
            if not 'itemid' in keys:
                raise RuntimeError('missing itemid column')

            # other lines are items
            line = handle.readline()
            while line:
                # remove comments
                line = regex_C.sub('', line).strip()

                # fix True and False
                line = regex_T.sub('1', line)
                line = regex_F.sub('0', line)

                # ignore empty lines
                if line:
                    # split into tokens
                    tokens = map(lambda x : x.strip(), line.split(','))

                    # check for new title line
                    if set(tokens).issubset(pydarkstar.item.Item.keys):
                        keys = tokens

                        # check for primary key
                        if not 'itemid' in keys:
                            raise RuntimeError('missing itemid column')

                    # validate line
                    elif set(tokens).intersection(pydarkstar.item.Item.keys):
                        raise RuntimeError('something wrong with line')

                    # process normal line
                    else:
                        # try to evaluate tokens
                        for i, token in enumerate(tokens):
                            try:
                                token = eval(token)
                            except SyntaxError:
                                pass
                            except NameError:
                                pass

                            # process missing tokens
                            if isinstance(token, str) and not token:
                                token = None

                            tokens[i] = token

                        # map values
                        kwargs = { k : None for k in keys }
                        for i in range(len(tokens)):
                            kwargs[keys[i]] = tokens[i]

                        # add new item
                        self.add(**kwargs)

                # read next line
                line = handle.readline()

    def savecsv(self, fname):
        with open(fname, 'wb') as handle:
            handle.write('{}\n'.format(','.join(pydarkstar.item.Item.keys)))
            for i in self.items:
                handle.write('{}\n'.format(self.items[i]))

if __name__ == '__main__':
    pass
