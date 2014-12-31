"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import pydarkstar.darkobject
import pydarkstar.item
import collections
import re
import os

class ItemList(pydarkstar.darkobject.DarkObject):
    """
    Container for Item objects.
    """
    def __init__(self):
        super(ItemList, self).__init__()
        self.items = collections.OrderedDict()

    def add(self, itemid, *args, **kwargs):
        """
        Add Item to ItemList.  Item must not already exist.

        .. seealso:: py:class:`pydarkstar.item.Item`
        """
        i = pydarkstar.item.Item(itemid, *args, **kwargs)
        if i.itemid in self.items:
            raise KeyError('duplicate item found: %d' % i.itemid)
        self.items[i.itemid] = i
        return i

    def set(self, *itemids, **kwargs):
        """
        Set Item(s) properties.
        """
        for itemid in itemids:
            i = self[itemid]
            for k in kwargs:
                if hasattr(i, k):
                    setattr(i, k, kwargs[k])
                else:
                    raise KeyError('%s' % str(k))

    def get(self, itemid):
        """
        Get Item by itemid.
        """
        return self.items[itemid]

    def __getitem__(self, itemid):
        return self.items[itemid]

    def __len__(self):
        return len(self.items)

    def loadcsv(self, fname):
        """
        Load Item(s) from CSV file.

        Columns are Item attributes.  The 'itemid' column is required.

        :param fname: name of file
        """
        regex_C = re.compile(r'#.*$')

        regex_T = '[{0}{1}]?True[{0}{1}]?'.format('"', "'")
        regex_T = re.compile(regex_T, re.IGNORECASE)

        regex_F = '[{0}{1}]?False[{0}{1}]?'.format('"', "'")
        regex_F = re.compile(regex_F, re.IGNORECASE)

        self.info('load %s', fname)
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

    @staticmethod
    def _write_objs(handle, *objs, **kwargs):
        """
        Helper method for writing CSV file.
        """
        a = kwargs.pop('a', '>')
        w = kwargs.pop('w', 16)
        _format = ', '.join([r'{:{a}{w}}'] * len(objs)) + '\n'
        handle.write(_format.format(*objs, a=a, w=w))

    def savecsv(self, fname, itertitle=100):
        """
        Save Item data to CSV file.

        :param fname: name of file
        """
        if os.path.exists(fname):
            self.info('overwriting file...')
            self.info('save %s', fname)
        else:
            self.info('save %s', fname)

        with open(fname, 'wb') as handle:
            for j, i in enumerate(self.items):
                if j % itertitle == 0:
                    self._write_objs(handle, *pydarkstar.item.Item.keys)
                self._write_objs(handle, *self.items[i].values)

if __name__ == '__main__':
    pass
