import logging
import time

import bs4
import requests
from bs4 import BeautifulSoup

from ffxiahbot.darkobject import DarkObject

TIMEOUT: int = 1024


class Scrubber(DarkObject):
    def __init__(self):
        super().__init__()

    def scrub(self):
        """
        Get item metadata.
        """
        return {}

    # noinspection PyBroadException
    @staticmethod
    def soup(url, absolute: bool = False, **kwargs):
        """
        Open URL and create tag soup.

        :param url: website string
        :type url: str

        :param absolute: perform double get request to find absolute url
        :type absolute: bool
        """
        handle = ""
        max_tries = 10
        for i in range(max_tries):
            # noinspection PyPep8
            try:
                if absolute:
                    url = requests.get(url, timeout=TIMEOUT).url
                handle = requests.get(url, params=kwargs, timeout=TIMEOUT).text
                break
            except Exception:
                logging.exception("urlopen failed (attempt %d)", i + 1)
                if i == max_tries - 1:
                    logging.exception("the maximum urlopen attempts have been reached")
                    raise
                time.sleep(1)

        try:
            s = BeautifulSoup(handle, features="html5lib")
        except bs4.FeatureNotFound:
            s = BeautifulSoup(handle, features="html.parser")

        return s


if __name__ == "__main__":
    pass
