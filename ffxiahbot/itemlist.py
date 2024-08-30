from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ffxiahbot.item import Item, item_csv_title_str, item_csv_value_str
from ffxiahbot.logutils import logger


@dataclass
class ItemList:
    """
    Container for Item objects.
    """

    items: dict[int,] = field(default_factory=dict)

    @classmethod
    def from_csv(cls, *csv_paths: Path) -> ItemList:
        """
        Create ItemList from CSV file(s).

        Args:
            *csv_paths: The path(s) to the CSV file(s).

        Returns:
            ItemList: The ItemList object created from the CSV file(s).
        """
        # make sure there is data
        if not csv_paths:
            raise RuntimeError("missing item data CSV!")

        # load data
        item_list = cls()
        logger.info("loading item data...")
        for csv_path in csv_paths:
            item_list.load_csv(csv_path)

        return item_list

    def add(self, itemid: int, *args: Any, **kwargs: Any) -> Item:
        """
        Add Item to ItemList.  Item must not already exist.

        Args:
            itemid: The item id.
            *args: The arguments to pass to the Item constructor.
            **kwargs: The keyword arguments to pass to the Item constructor.

        Returns:
            Item: The Item object created.
        """
        item = Item(itemid, *args, **kwargs)
        if item.itemid in self.items:
            raise KeyError("duplicate item found: %d" % item.itemid)
        self.items[item.itemid] = item
        return item

    def set(self, *itemids: int, **kwargs: Any) -> None:
        """
        Set Item(s) properties.

        Args:
            *itemids: The item id(s) to set the properties for.
            **kwargs: The properties to set.

        Raises:
            KeyError: If a property is not found.
        """
        for itemid in itemids:
            i = self[itemid]
            for k in kwargs:
                if hasattr(i, k):
                    setattr(i, k, kwargs[k])
                else:
                    raise KeyError(f"{k!s}")

    def get(self, itemid: int) -> Item:
        """
        Get Item by itemid.

        Args:
            itemid: The item id.

        Returns:
            Item: The Item object.
        """
        return self.items[itemid]

    def __getitem__(self, itemid: int) -> Item:
        """
        Get Item by itemid.

        Args:
            itemid: The item id.

        Returns:
            Item: The Item object.
        """
        return self.items[itemid]

    def __len__(self) -> int:
        """
        Get the number of items in the ItemList.

        Returns:
            int: The number of items in the ItemList.
        """
        return len(self.items)

    def load_csv(self, csv_path: Path | str) -> None:  # noqa: C901
        """
        Load Item(s) from CSV file.

        Columns are Item attributes.  The 'itemid' column is required.

        Args:
            csv_path: The path to the CSV file.

        Raises:
            RuntimeError: If the itemid column is missing.
            RuntimeError: If an unknown column is found.
            RuntimeError: If something is wrong with a line.
        """
        regex_c = re.compile(r"#.*$")

        regex_t = "[{0}{1}]?True[{0}{1}]?".format('"', "'")
        regex_t = re.compile(regex_t, re.IGNORECASE)

        regex_f = "[{0}{1}]?False[{0}{1}]?".format('"', "'")
        regex_f = re.compile(regex_f, re.IGNORECASE)

        logger.info("load %s", csv_path)
        line_number = 0
        with open(csv_path) as handle:
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
                if k not in Item.keys:
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
                    if set(tokens).issubset(Item.keys):
                        keys = tokens

                        # check for primary key
                        if "itemid" not in keys:
                            raise RuntimeError(f"missing itemid column:\n\t{keys}")

                    # validate line
                    elif set(tokens).intersection(Item.keys):
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

    def save_csv(self, csv_path: Path, iter_title: int = 1024) -> None:
        """
        Save Item data to CSV file.

        Args:
            csv_path: The path to save the CSV file.
            iter_title: The number of items to write before writing the title row.
        """
        if csv_path.exists():
            logger.info("overwriting file...")
            logger.info("save %s", csv_path)
        else:
            logger.info("save %s", csv_path)

        with csv_path.open("w") as stream:
            for j, i in enumerate(self.items):
                if j % iter_title == 0:
                    stream.write(item_csv_title_str())
                stream.write(item_csv_value_str(self.items[i]))
