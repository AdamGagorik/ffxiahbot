from ..darkobject import DarkObject
from bs4 import BeautifulSoup

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

class Scrubber(DarkObject):
    def __init__(self, *args, **kwargs):
        super(Scrubber, self).__init__(*args, **kwargs)

    def scrub(self):
        """
        Get item metadata.
        """
        return {}

    @staticmethod
    def soup(url):
        """
        Open URL and create tag soup.

        :param url: website string
        :type url: str
        """
        handle = urlopen(url)
        s = BeautifulSoup(handle.read())
        return s

if __name__ == '__main__':
    pass