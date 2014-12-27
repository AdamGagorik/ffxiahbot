"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
from bs4 import BeautifulSoup
import urllib2
import logging

def soup(url):
    """
    Open URL and create tag soup.

    :param url: website string
    :type url: str
    """
    logging.info('open %s', url)
    handle = urllib2.urlopen(url)
    s = BeautifulSoup(handle.read())
    return s

if __name__ == '__main__':
    pass