from .scrubber import Scrubber
import concurrent.futures
import warnings
import pickle
import re
import os


SERVER_ID = {
    'bahamut': 1,
    'shiva': 2,
    'titan': 3,
    'ramuh': 4,
    'phoenix': 5,
    'carbuncle': 6,
    'fenrir': 7,
    'sylph': 8,
    'valefor': 9,
    'alexander': 10,
    'leviathan': 11,
    'odin': 12,
    'ifrit': 13,
    'diabolos': 14,
    'caitsith': 15,
    'quetzalcoatl': 16,
    'siren': 17,
    'unicorn': 18,
    'gilgamesh': 19,
    'ragnarok': 20,
    'pandemonium': 21,
    'garuda': 22,
    'cerberus': 23,
    'kujata': 24,
    'bismarck': 25,
    'seraph': 26,
    'lakshmi': 27,
    'asura': 28,
    'midgardsormr': 29,
    'fairy': 30,
    'remora': 31,
    'hades': 32
}

ID_SERVER = {v: k for k, v in SERVER_ID.items()}


class FFXIAHScrubber(Scrubber):
    """
    Get item data from ffxiah.com
    """
    def __init__(self):
        super(FFXIAHScrubber, self).__init__()

        # regular expressions
        self._regex_category = re.compile(r'/browse/(\d+)/?.*')
        self._regex_item = re.compile(r'/item/(\d+)')
        self._regex_name = re.compile(r'(.*?)\s*-?\s*(FFXIAH)?\.(com)?')

        # pickled file names
        self._pkl_item_ids = 'scrub_item_list.pkl'
        self._pkl_item_dat = 'scrub_item_info.pkl'
        self._server_id = 1
        self._save = True

    @property
    def save(self):
        return self._save

    @save.setter
    def save(self, value):
        self._save = bool(value)

    @property
    def server(self):
        return ID_SERVER[self.server_id]

    @property
    def server_id(self):
        return self._server_id

    @server_id.setter
    def server_id(self, value):
        if isinstance(value, int):
            assert value in SERVER_ID.values()
        else:
            value = SERVER_ID[value]
        self._server_id = value

    def scrub(self, force=False, threads=None, urls=None, ids=None):
        """
        Get item metadata main function.

        If the pkl files exist (from a previous run of this function), then the ids and/or data
        will just be loaded from those pkl files.  The force option allows you to ignore the
        pkl files and just redownload the data.

        The item ids can be loaded from category urls or simply passed as a list.  The urls
        can be generated automatically, in which case all possible items will be downloaded.

        :param force: ignore existing data and redownload
        :param threads: number of cpu threads to use while downloading
        :param urls: list of category urls
        :param ids: set of item ids

        :type force: bool
        :type threads: int
        :type urls: list, None
        :type ids: set, list, None
        """
        # force a redownload of all data
        if force:
            self.debug('forcing redownload of data')

            # get ids
            if ids is None:
                # get urls
                if urls is None:
                    urls = self._get_category_urls()
                self.debug('# urls = %d', len(urls))

                ids = self._get_itemids(urls, threads)

                # save to file
                self._save_item_ids(ids)

            else:
                self.debug('using passed ids')
                ids = set(ids)

                if urls is not None:
                    warnings.warn('passed urls ignored')

            # from internet
            failed, data = self._get_item_data(ids, threads=threads)

            # save to file
            self._save_item_dat(data)

            self.debug('item count = %d', len(ids))
            self.debug('data count = %d', len(data))
            return failed, data

        else:
            # data exists already
            if os.path.exists(self._pkl_item_dat):
                data = self._load_item_dat()

                if ids is not None:
                    warnings.warn('passed ids ignored')

                if os.path.exists(self._pkl_item_ids):
                    warnings.warn('%s ignored' % self._pkl_item_ids)

                self.debug('data count = %d', len(data))
                return data

            # get ids
            if ids is None:

                # from file
                if os.path.exists(self._pkl_item_ids):
                    ids = self._load_item_ids()

                # from internet
                else:
                    # get urls
                    if urls is None:
                        urls = self._get_category_urls()
                    self.debug('# urls = %d', len(urls))

                    ids = self._get_itemids(urls, threads)

                    # save to file
                    self._save_item_ids(ids)
            else:
                self.debug('using passed ids')
                ids = set(ids)

                if urls is not None:
                    warnings.warn('passed urls ignored')

            # from file
            if os.path.exists(self._pkl_item_dat):
                raise RuntimeError('%s exists' % self._pkl_item_dat)

            # from internet
            failed, data = self._get_item_data(ids, threads=threads)

            # save to file
            self._save_item_dat(data)

            self.debug('item count = %d', len(ids))
            self.debug('data count = %d', len(data))
            return failed, data

    def _load_item_ids(self):
        """
        Load item ids from pkl file.
        """
        if not os.path.exists(self._pkl_item_ids):
            return set()

        self.debug('load %s', self._pkl_item_ids)
        with open(self._pkl_item_ids, 'rb') as handle:
            ids = pickle.load(handle)
        return set(ids)

    def _load_item_dat(self):
        """
        Load item dat from pkl file.
        """
        if not os.path.exists(self._pkl_item_dat):
            return dict()

        self.debug('load %s', self._pkl_item_dat)
        with open(self._pkl_item_dat, 'rb') as handle:
            dat = pickle.load(handle)
        return dict(dat)

    def _save_item_ids(self, ids):
        """
        save item ids to pkl file.
        """
        if self._save:
            self.debug('save %s', self._pkl_item_ids)
            with open(self._pkl_item_ids, 'wb') as handle:
                pickle.dump(ids, handle, pickle.HIGHEST_PROTOCOL)

    def _save_item_dat(self, dat):
        """
        save item dat to pkl file.
        """
        if self._save:
            self.debug('save %s', self._pkl_item_dat)
            with open(self._pkl_item_dat, 'wb') as handle:
                pickle.dump(dat, handle, pickle.HIGHEST_PROTOCOL)

    # step 1
    def _get_category_urls(self):
        """
        Parse http://www.ffxiah.com/browse to get URLs of the
         form http://www.ffxiah.com/{CategoryNumber}
        """
        self.debug('getting category urls')

        # the browse section of FFXIAH has a list of urls with category numbers
        path = 'http://www.ffxiah.com/browse'
        self.debug('open %s', path)
        soup = self.soup(path)
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
        urls.sort(key=lambda x: list(map(float, re.findall(r'\d+', x))))

        return urls

    # step 2
    def _get_itemids(self, urls, threads):
        """
        Scrub urls of the form http://www.ffxiah.com/{CategoryNumber} for itemids.

        :param urls: category urls
        """
        self.info('getting itemids')

        items = set()
        if threads is None or threads != 1:
            threads = threads if threads > 1 else None
            self.info('executing in parallel with threads=%s', 'ALL' if threads is None else threads)
            with concurrent.futures.ThreadPoolExecutor(max_workers=threads, thread_name_prefix='ExThread') as executor:
                futures = {}
                for i, url in enumerate(urls):
                    self.info('submit category %02d/%02d : %s', i + 1, len(urls), url)
                    futures[executor.submit(self._get_itemids_for_category_url, url)] = url

                for future in concurrent.futures.as_completed(futures):
                    self.info('return category %02d/%02d : %s', i + 1, len(urls), url)
                    url = futures[future]
                    items.update(future.result())
        else:
            for i, url in enumerate(urls):
                self.info('category %02d/%02d : %s', i + 1, len(urls), url)
                items.update(self._get_itemids_for_category_url(url))

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
            return set()

        # look for table body
        tbody = table.find('tbody')
        if not tbody:
            self.error('failed to parse <tbody>')
            return set()

        # look for table rows
        trs = tbody.find_all('tr')
        if not trs:
            self.error('failed to parse <tr>')
            return set()

        # loop table rows
        items = set()
        for j, row in enumerate(trs):
            # look for 'a' tag
            a = row.find('a')

            if a is not None:
                # look for href attr
                href = a.get('href')

                if href is not None:
                    # make sure href matches /item/{number}
                    try:
                        item = int(self._regex_item.match(href).group(1))
                        items.add(item)
                        # logging.debug('found %s', href)

                    except (ValueError, IndexError):
                        self.exception('failed to extract itemid!\n\n\trow %d of %s\n\n%s\n\n',
                                       j, url, row)
                else:
                    self.error('failed to extract href!\n\n\trow %d of %s\n\n%s\n\n',
                               j, url, row)
            else:
                self.error("failed to extract 'a' tag!\n\n\trow %d of %s\n\n%s\n\n",
                           j, url, row)

        # make sure we found something
        if not items:
            self.error('could not find any itemids!')
            return set()

        return items

    # step 3
    def _get_item_data(self, itemids, threads=None):
        """
        Get metadata for many items.

        :param itemids: item numbers
        :param threads: number of cpu threads to use

        :type itemids: list, set
        :type threads: int
        """
        self.info('getting data')

        data = {}
        failed = {}
        # get data from itemids
        if threads is None or threads != 1:
            threads = threads if threads > 1 else None
            self.info('executing in parallel with threads=%s', 'ALL' if threads is None else threads)
            with concurrent.futures.ThreadPoolExecutor(max_workers=threads, thread_name_prefix='ExThread') as executor:
                futures = {
                    executor.submit(self._get_item_data_for_itemid, itemid,
                                    index=i, total=len(itemids)): itemid
                    for i, itemid in enumerate(itemids)
                }
                for future in concurrent.futures.as_completed(futures):
                    itemid = futures[future]
                    try:
                        result = future.result()
                        data[itemid] = result
                    except Exception as e:
                        self.exception('failed to scrub %d!', itemid)
                        failed[itemid] = e
        else:
            for i, itemid in enumerate(itemids):
                try:
                    result = self._get_item_data_for_itemid(itemid, index=i, total=len(itemids))
                    data[itemid] = result
                except Exception as e:
                    self.exception('failed to scrub %d!', itemid)
                    failed[itemid] = e

        if failed:
            for itemid in failed:
                self.error('failed to scrub %d!', itemid)

        return failed, data

    # step 3.1
    def _get_item_data_for_itemid(self, itemid, index=0, total=0):
        """
        Get metadata for single item.

        :param itemid: item number
        :type itemid: int
        """
        if total > 0:
            percent = float(index) / float(total) * 100.0
        else:
            percent = 0.0

        data = {'name': None, 'itemid': itemid}
        url = self._create_item_url(itemid)

        # create tag soup
        self.debug('open server=%s (%06d/%06d,%6.2f) %s', self.server, index, total, percent, url)
        soup = self.soup(url, absolute=True, sid=self.server_id)

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

        # extract rate
        for tag in soup.find_all('span', 'sales-rate'):
            try:
                data['rate'] = float(tag.text)
            except (AttributeError, ValueError):
                pass

        # fix key
        data = self._fix_stack_price_key(data)

        return data

    def _get_item_data_for_itemid_map(self, args):
        return self._get_item_data_for_itemid(*args)

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
        """
        Fix dictionary key.

        :param data: dictionary
        :type data: dict
        """
        new_key = r'stack price'

        for key in list(data.keys()):
            if 'stack' in key.lower():
                data[new_key] = data[key]

        return data


def extract(data, itemid, **kwargs):
    """
    Extract item data from scrubbed info.
    """
    # singles
    try:
        price_single, sell_single = data[itemid]['median'], True

        # do not sell items without a price
        if price_single <= 0:
            price_single, sell_single = None, False

    except KeyError:
        price_single, sell_single = None, False

    # stacks
    try:
        price_stacks, sell_stacks = data[itemid]['stack price'], True

        # do not sell items without a price
        if price_stacks <= 0:
            price_stacks, sell_stacks = None, False

    except KeyError:
        price_stacks, sell_stacks = None, False

    # the name doesn't really matter
    try:
        name = data[itemid]['name']
    except KeyError:
        name = None

    result = dict(name=name,
                  price_single=price_single, stock_single=5, sell_single=sell_single, buy_single=True, rate_single=1.0,
                  price_stacks=price_stacks, stock_stacks=5, sell_stacks=sell_stacks, buy_stacks=True, rate_stacks=1.0)
    result.update(**kwargs)

    return result


if __name__ == '__main__':
    pass
