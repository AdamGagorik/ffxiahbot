from ..darkobject import DarkObject
from bs4 import BeautifulSoup
import logging
import time


from urllib.request import urlopen


class Scrubber(DarkObject):
    def __init__(self):
        super(Scrubber, self).__init__()

    def scrub(self):
        """
        Get item metadata.
        """
        return {}

    # noinspection PyBroadException
    @staticmethod
    def soup(url):
        """
        Open URL and create tag soup.

        :param url: website string
        :type url: str
        """
        handle = ''
        max_tries = 10
        for i in range(max_tries):
            # noinspection PyPep8
            try:
                handle = urlopen(url)
                handle = handle.read()
                break
            except:
                logging.exception('urlopen failed (attempt %d)', i + 1)
                if i == max_tries - 1:
                    logging.error('the maximum urlopen attempts have been reached')
                    raise
                time.sleep(1)

        s = BeautifulSoup(handle)
        return s


if __name__ == '__main__':
    pass
