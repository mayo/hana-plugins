from __future__ import absolute_import
import json
import logging
import os
import time
import urlparse
import CloudFlare
from hana.errors import HanaPluginError

CF_PURGE_LIMIT = 500

class PurgeCache(object):
    def __init__(self, base_url, cache_file, cf_email=None, cf_token=None, wait_for_purge=True, empty_cache_purge=False):
        self.logger = logging.getLogger('{}.{}'.format(self.__module__, self.__class__.__name__))

        self.base_url = base_url
        self.cache_file = cache_file
        self.cache = {}

        self.cf_email = cf_email
        self.cf_token = cf_token

        self.wait_for_purge = wait_for_purge
        self.empty_cache_purge = empty_cache_purge

        if os.path.exists(self.cache_file):
            with open(self.cache_file) as fp:
                self.logger.debug('Loading cache file')
                self.cache = json.load(fp)

        self.empty_cache = len(self.cache) == 0

    def _cf_purge(self, files, wait=False):
        self.logger.info('Purging Cache')
        params = {}

        if self.cf_email:
            params['email'] = self.cf_email

        if self.cf_token:
            params['token'] = self.cf_token

        cf_api = CloudFlare.CloudFlare(**params)

        domain = urlparse.urlparse(self.base_url).netloc

        zone_id = cf_api.zones.get(params={'name': domain})[0]['id']

        urls = [urlparse.urljoin(self.base_url, fn) for fn in files]

        for idx in xrange(0, len(urls), CF_PURGE_LIMIT):
            url_subset = urls[idx:idx+CF_PURGE_LIMIT]
            self.logger.info('Purging %d/%d files', len(url_subset), len(urls))

            try: 
                res = cf_api.zones.purge_cache.delete(zone_id, data={'files':url_subset})
            except CloudFlare.exceptions.CloudFlareAPIError as e:
                raise HanaPluginError(e)

        if wait:
            self.logger.info('Waiting 30 seconds for cache flush')

            ts = time.time()

            while time.time() - ts < 30:
                 time.sleep(1)


    def __call__(self, files, hana):
        purge_files = []

        for filename, hfile in files:
            file_sha1sum = hfile.sha1sum()

            # skip files that don't need updating
            if file_sha1sum == self.cache.get(filename):
                continue

            # update file checksum
            self.cache[filename] = file_sha1sum

            # don't purge if cache is empty, always purge if requested
            if not self.empty_cache or self.empty_cache_purge:
                purge_files.append(filename)

        purge_files.append('https://oyam.ca/404.html')

        if purge_files:
            self._cf_purge(purge_files, wait=self.wait_for_purge)
        else:
            self.logger.debug('No files to purge')

        if self.cache_file:
            self.logger.debug('Writing cache file')

            with open(self.cache_file, 'w') as fp:
                json.dump(self.cache, fp)

