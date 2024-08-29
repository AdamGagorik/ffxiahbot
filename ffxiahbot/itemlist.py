import ast
import collections
import os
import re

from ffxiahbot import item
from ffxiahbot.darkobject import DarkObject


class ItemList(DarkObject):
    """
    Container for Item objects.
    """

    def __init__(self):
        super().__init__()
        self.items = collections.OrderedDict()

    @classmethod
    def from_csv(cls, *data):
        """
        Create ItemList from CSV file(s).
        """
        # make sure there is data
        if not data:
            raise RuntimeError("missing item data CSV!")

        # load data
        obj = ItemList()
        obj.info("loading item data...")
        for f in data:
            obj.loadcsv(f)

        return obj

    def add(self, itemid, *args, **kwargs):
        """
        Add Item to ItemList.  Item must not already exist.

        .. seealso:: py:class:`ffxiahbot.item.Item`
        """
        i = item.Item(itemid, *args, **kwargs)
        if i.itemid in self.items:
            raise KeyError("duplicate item found: %d" % i.itemid)
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
                    raise KeyError(f"{k!s}")

    def get(self, itemid):
        """
        Get Item by itemid.
        """
        return self.items[itemid]

    def __getitem__(self, itemid):
        return self.items[itemid]

    def __len__(self):
        return len(self.items)

    def loadcsv(self, fname):  # noqa: C901
        """
        Load Item(s) from CSV file.

        Columns are Item attributes.  The 'itemid' column is required.

        :param fname: name of file
        """
        regex_c = re.compile(r"#.*$")

        regex_t = "[{0}{1}]?True[{0}{1}]?".format('"', "'")
        regex_t = re.compile(regex_t, re.IGNORECASE)

        regex_f = "[{0}{1}]?False[{0}{1}]?".format('"', "'")
        regex_f = re.compile(regex_f, re.IGNORECASE)

        self.info("load %s", fname)
        line_number = 0
        with open(fname) as handle:
            # first line is item titles
            line = handle.readline()
            line_number += 1

            # ignore comments
            line = regex_c.sub("", line).strip()

            # split into tokens
            keys = line.split(",")
            keys = [x.strip().lower() for x in keys]

            # make sure keys are valid
            for k in keys:
                if k not in item.Item.keys:
                    raise RuntimeError(f"unknown column: {k}")

            # check for primary key
            if "itemid" not in keys:
                raise RuntimeError(f"missing itemid column:\n\t{keys}")

            # other lines are items
            line = handle.readline()
            line_number += 1

            while line:
                # remove comments
                line = regex_c.sub("", line).strip()

                # fix True and False
                line = regex_t.sub("1", line)
                line = regex_f.sub("0", line)

                # ignore empty lines
                if line:
                    # split into tokens
                    tokens = [x.strip() for x in line.split(",")]

                    # check for new title line
                    if set(tokens).issubset(item.Item.keys):
                        keys = tokens

                        # check for primary key
                        if "itemid" not in keys:
                            raise RuntimeError(f"missing itemid column:\n\t{keys}")

                    # validate line
                    elif set(tokens).intersection(item.Item.keys):
                        raise RuntimeError("something wrong with line %d" % line_number)

                    # process normal line
                    else:
                        # try to evaluate tokens
                        for i, token in enumerate(tokens):
                            try:
                                token = ast.literal_eval(token)
                            except SyntaxError:
                                pass
                            except ValueError:
                                pass
                            except NameError:
                                pass

                            # process missing tokens
                            if isinstance(token, str) and not token:
                                token = None

                            tokens[i] = token

                        # map values
                        kwargs = {k: None for k in keys}
                        for i in range(len(tokens)):
                            kwargs[keys[i]] = tokens[i]

                        # add new item
                        self.add(**kwargs)

                # read next line
                line = handle.readline()
                line_number += 1

    def savecsv(self, fname, itertitle=100):
        """
        Save Item data to CSV file.

        :param fname: name of file
        :param itertitle: how often to write title line
        """
        if os.path.exists(fname):
            self.info("overwriting file...")
            self.info("save %s", fname)
        else:
            self.info("save %s", fname)

        with open(fname, "w") as handle:
            for j, i in enumerate(self.items):
                if j % itertitle == 0:
                    handle.write(item.title_str())
                handle.write(item.value_str(self.items[i]))


if __name__ == "__main__":
    pass
