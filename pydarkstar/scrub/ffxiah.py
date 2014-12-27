"""
.. moduleauthor:: Adam Gagorik <adam.gagorik@gmail.com>
"""
import pydarkstar.scrub.scrubber
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

        # pickled file names
        self._pkl_item_ids = 'itemids.pkl'
        self._pkl_item_dat = 'itemdat.pkl'

    def scrub(self, force=False, threads=-1, urls=None, ids=None):
        """
        Get item metadata main function.
        """
        # force a redownload of all data
        if force:
            # get ids
            if ids is None:
                # get urls
                if urls is None:
                    urls = self._get_category_urls()
                ids  = self._get_itemids(urls)
            data = self._get_item_data(ids, threads=threads)

        else:
            # get ids
            if ids is None:

                # from file
                if os.path.exists(self._pkl_item_ids):
                    with open(self._pkl_item_ids, 'rb') as handle:
                        ids = pickle.load(handle)

                # from internet
                else:
                    # get urls
                    if urls is None:
                        urls = self._get_category_urls()

                    ids = self._get_itemids(urls)

            # from file
            if os.path.exists(self._pkl_item_dat):
                with open(self._pkl_item_dat, 'rb') as handle:
                    data = pickle.load(handle)

            # from internet
            else:
                data = self._get_item_data(ids, threads=threads)

        # save to file
        with open(self._pkl_item_ids, 'wb') as handle:
            pickle.dump(ids, handle, pickle.HIGHEST_PROTOCOL)

        # save to file
        with open(self._pkl_item_dat, 'wb') as handle:
            pickle.dump(data, handle, pickle.HIGHEST_PROTOCOL)

        return data

    # step 1
    def _get_category_urls(self):
        """
        Parse http://www.ffxiah.com/browse to get URLs of the
         form http://www.ffxiah.com/{CategoryNumber}
        """

        # the browse section of FFXIAH has a list of urls with category numbers
        soup = self.soup('http://www.ffxiah.com/browse')
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
                            self.debug('category %s', href)
                        else:
                            self.debug('skipping %s', href)

                    except (ValueError, IndexError):
                        self.exception('failed to extract category')
                else:
                    self.debug('ignoring %s', href)

        # sort the urls
        urls.sort(key=lambda x : map(float, re.findall('\d+', x)))

        return urls

    # step 2
    def _get_itemids(self, urls):
        """
        Scrub urls of the form http://www.ffxiah.com/{CategoryNumber} for itemids.

        :param urls: category urls
        """
        self.info('getting itemids')

        items = []
        for i, url in enumerate(urls):
            self.info('category %02d/%02d', i + 1, len(urls))
            items.extend(self._get_itemids_for_category_url(url))

        return items

    # step 2.1
    def _get_itemids_for_category_url(self, url):
        """
        Scrub url of the form http://www.ffxiah.com/{CategoryNumber} for itemids.

        :param url: category url
        """
        # create tag soup
        soup = self.soup(url)

        # look for table class
        table = soup.find('table', class_='stdlist')
        if not table:
            self.error('failed to parse <table>')
            return

        # look for table body
        tbody = table.find('tbody')
        if not tbody:
            self.error('failed to parse <tbody>')
            return

        # look for table rows
        trs = tbody.find_all('tr')
        if not trs:
            self.error('failed to parse <tr>')
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
                    self.exception('failed to extract itemid!\n\n\trow %d of %s\n\n%s\n\n',
                        j, url, row)
            else:
                self.error('failed to extract href!\n\n\trow %d of %s\n\n%s\n\n',
                    j, url, row)

        # make sure we found something
        if not items:
            self.error('could not find any itemids!')
            return []

        return items

    # step 3
    def _get_item_data(self, itemids, threads=-1):
        """
        Get metadata for many items.

        :param itemids: item numbers
        :param threads: number of cpu threads to use

        :type itemids: list
        :type threads: int
        """
        self.info('getting itemdata')
        self.info('threads = %d', threads)

        # get data from itemids
        if threads > 1:
            from multiprocessing.dummy import Pool as ThreadPool
            pool = ThreadPool(threads)
            data = pool.map(self._get_item_data_for_itemid, itemids)
            data = {d['itemid'] : d for d in data}
        else:
            data = {}
            for i, itemid in enumerate(itemids):
                data[itemid] = self._get_item_data_for_itemid(itemid)

        return data

    # step 3.1
    def _get_item_data_for_itemid(self, itemid):
        """
        Get metadata for single item.

        :param itemid: item number
        :type itemid: int
        """
        data = {'name' : None, 'itemid' : itemid}
        url = self._create_item_url(itemid)

        # create tag soup
        soup = self.soup(url)

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