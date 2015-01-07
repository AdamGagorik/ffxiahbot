import pydarkstar.darkobject
from bs4 import BeautifulSoup
import urllib2

class Scrubber(pydarkstar.darkobject.DarkObject):
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
        handle = urllib2.urlopen(url)
        s = BeautifulSoup(handle.read())
        return s

if __name__ == '__main__':
    pass