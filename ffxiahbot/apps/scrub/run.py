"""
Create item database.
"""

import logging
import os
import re

from ffxiahbot import common, logutils
from ffxiahbot.apps.scrub.options import Options
from ffxiahbot.itemlist import ItemList
from ffxiahbot.scrubbing import ffxiah


def main():
    """
    Main function.
    """
    # get options
    opts = Options()

    # check output file name validity
    oname = os.path.abspath("{}.csv".format(re.sub(r"\.csv$", "", opts.stub)))
    if not opts.overwrite and not opts.backup and os.path.exists(oname):
        logging.error("output file already exists!\n\t%s", oname)
        logging.error("please use --overwrite or --backup")
        exit(-1)

    # scub data
    scrubber = ffxiah.FFXIAHScrubber()
    scrubber.server_id = opts.server
    scrubber.save = False
    failed, data = scrubber.scrub(force=True, threads=opts.threads, urls=opts.urls, ids=opts.itemids)

    if data:
        # create item list from data
        ilist = ItemList()
        for itemid in sorted(data.keys()):
            kwargs = ffxiah.extract(data, itemid, stock_single=opts.stock_single, stock_stacks=opts.stock_stacks)
            ilist.add(itemid, **kwargs)

    # backup file
    if opts.backup:
        common.backup(oname, copy=True)

    # overwrites if exists, but we checked already
    ilist.savecsv(oname)

    if not data:
        raise RuntimeError("no items were scrubbed!")

    if failed:
        raise RuntimeError("not all item ids were scrubbed, but a CSV was still saved!")


def cleanup():
    logging.info("exit\n")


if __name__ == "__main__":
    with logutils.capture():
        main()
    cleanup()
