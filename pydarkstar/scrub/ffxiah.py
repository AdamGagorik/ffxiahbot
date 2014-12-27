"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import pydarkstar.scrub.scrubber
import pydarkstar.scrub.common
import logging
import pickle
import re
import os

class FFXIAHScrubber(pydarkstar.scrub.scrubber.Scrubber):
    """
    Get item data from ffxiah.com
    """
    def __init__(self, *args, **kwargs):
        super(FFXIAHScrubber, self).__init__(*args, **kwargs)

        # regular expressions
        self._regex_category = re.compile(r'/browse/(\d+)/?.*')
        self._regex_item     = re.compile(r'/item/(\d+)')
        self._regex_name     = re.compile(r'(.*?)\s*-?\s*(FFXIAH)?\.(com)?')

    def scrub(self):
        """
        Get item metadata.
        """
        return {}

    # step 1
    def _get_category_urls(self):
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
                match = self._regex_category.match(href)
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

    # step 2
    def _get_itemids(self, urls=None, force=False, save='itemids.pkl'):
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
            urls = self._get_category_urls()

            # parse items
            for i, url in enumerate(urls):
                logging.info('category %02d/%02d', i + 1, len(urls))
                items.extend(self._get_itemids_for_category_url(url))

        # soft load
        else:

            # load items from file
            if save and os.path.exists(save):
                with open(save, 'rb') as handle:
                    items = pickle.load(handle)

            else:
                # parse urls
                if not urls:
                    urls = self._get_category_urls()

                # parse items
                for i, url in enumerate(urls):
                    logging.info('category %02d/%02d', i + 1, len(urls))
                    items.extend(self._get_itemids_for_category_url(url))

        # save items to file
        if save:
            with open(save, 'wb') as handle:
                pickle.dump(items, handle, pickle.HIGHEST_PROTOCOL)

        return items

    # step 2.1
    def _get_itemids_for_category_url(self, url):
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
                    item = int(self._regex_item.match(href).group(1))
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

    # step 3.1
    def _get_item_data_for_itemid(self, itemid):
        """
        Get metadata for single item from www.ffxiah.com.
        """
        data = {'name' : None, 'itemid' : itemid}
        url = self._create_item_url(itemid)

        # create tag soup
        soup = pydarkstar.scrub.common.soup(url)

        # extract name
        try:
            data.update(name=self._regex_name.match(soup.title.text).group(1))
        except AttributeError:
            data.update(name=None)

        # extract numbers
        for tag in soup.find_all('span', 'number-format'):
            try:
                key = tag.parent.find_previous_sibling().text.lower()
                data[key] = int(float(tag.text))
            except (AttributeError, ValueError):
                pass

        # fix key
        data = self._fix_stack_price_key(data)

        return data

    # step 3.1.1
    @staticmethod
    def _create_item_url(itemid):
        """
        Create URL from itemid.

        :param itemid: item number
        :type itemid: int
        """
        return 'http://www.ffxiah.com/item/{item}'.format(item=itemid)

    # step 3.1.2
    @staticmethod
    def _fix_stack_price_key(data):
        old_key = u'stack\xa0price'
        new_key = r'stack price'
        if data.has_key(old_key):
            data[new_key] = data[old_key]
            del data[old_key]

        return data

if __name__ == '__main__':
    pass