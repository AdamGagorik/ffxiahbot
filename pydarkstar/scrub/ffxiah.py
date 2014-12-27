"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import pydarkstar.scrub.common
import logging
import pickle
import re
import os

_regex_category = re.compile(r'/browse/(\d+)/?.*')
_regex_item = re.compile(r'/item/(\d+)')

def getCategoryURLs():
    """
    Parse http://www.ffxiah.com/browse to get URLs of the
     form http://www.ffxiah.com/{CategoryNumber}
    """

    # the browse section of FFXIAH has a list of urls with category numbers
    soup = pydarkstar.scrub.common.soup('http://www.ffxiah.com/browse')
    urls = []
    for tag in soup.find_all('a'):
        if tag.has_attr('href'):
            href = tag.get('href')
            match = _regex_category.match(href)
            if match:
                try:
                    category = int(match.group(1))

                    if category < 240:
                        urls.append('http://www.ffxiah.com{href}'.format(href=href))
                        logging.debug('category %s', href)
                    else:
                        logging.debug('skipping %s', href)

                except (ValueError, IndexError):
                    logging.exception('failed to extract category')
            else:
                logging.debug('ignoring %s', href)

    # sort the urls
    urls.sort(key=lambda x : map(float, re.findall('\d+', x)))

    return urls

def scrubCategoryURL(url):
    """
    Scrub url of the form http://www.ffxiah.com/{CategoryNumber} for itemids.

    :param url: category url
    """
    # create tag soup
    soup = pydarkstar.scrub.common.soup(url)

    # look for table class
    table = soup.find('table', class_='stdlist')
    if not table:
        logging.error('failed to parse <table>')
        return

    # look for table body
    tbody = table.find('tbody')
    if not tbody:
        logging.error('failed to parse <tbody>')
        return

    # look for table rows
    trs = tbody.find_all('tr')
    if not trs:
        logging.error('failed to parse <tr>')
        return

    # loop table rows
    items = []
    for j, row in enumerate(trs):

        # look for href
        href = row.find('a').get('href')

        if not href is None:
            # make sure href matches /item/{number}
            try:
                item = int(_regex_item.match(href).group(1))
                items.append(item)
                #logging.debug('found %s', href)

            except (ValueError, IndexError):
                logging.exception('failed to extract itemid!\n\n\trow %d of %s\n\n%s\n\n',
                    j, url, row)
        else:
            logging.error('failed to extract href!\n\n\trow %d of %s\n\n%s\n\n',
                j, url, row)

    # make sure we found something
    if not items:
        logging.error('could not find any itemids!')
        return []

    return items

def getItemids(urls=None, force=False, save='itemids.pkl'):
    """
    Scrub urls of the form http://www.ffxiah.com/{CategoryNumber} for itemids.

    If no urls are given, then they are obtained using getCategoryURLs()
    If force, then save and urls are ignored.

    :param urls: list of category urls
    :param force: do not load from file
    :param save: pickle file
    """
    logging.info('getting itemids')
    items = []

    # hard load
    if force:

        # parse urls
        urls = getCategoryURLs()

        # parse items
        for i, url in enumerate(urls):
            logging.info('category %02d/%02d', i + 1, len(urls))
            items.extend(scrubCategoryURL(url))

    # soft load
    else:

        # load items from file
        if save and os.path.exists(save):
            with open(save, 'rb') as handle:
                items = pickle.load(handle)

        else:
            # parse urls
            if not urls:
                urls = getCategoryURLs()

            # parse items
            for i, url in enumerate(urls):
                logging.info('category %02d/%02d', i + 1, len(urls))
                items.extend(scrubCategoryURL(url))

    # save items to file
    if save:
        with open(save, 'wb') as handle:
            pickle.dump(items, handle, pickle.HIGHEST_PROTOCOL)

    return items

if __name__ == '__main__':
    pass