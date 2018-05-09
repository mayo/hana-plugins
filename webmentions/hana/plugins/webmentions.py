from __future__ import absolute_import
import json
import logging
import os
import re
import urlparse
import urllib3

import requests
import ronkyuu

WEBMENTION_META_KEY = '_webmentions'

class FindWebmentions(object):
    def __init__(self, exclude_domains=(), webmention_meta_key=WEBMENTION_META_KEY, allow_insecure_https=False, cache_file=None):
        self.logger = logging.getLogger('{}.{}'.format(self.__module__, self.__class__.__name__))

        self.exclude_domains = list(exclude_domains)
        self.webmention_meta_key = webmention_meta_key
        self.cache_file = cache_file
        self.cache = {}

        if self.cache_file:
            if os.path.exists(self.cache_file):
                with open(self.cache_file) as fp:
                    self.cache = json.load(fp)

        if allow_insecure_https:
            urllib3.disable_warnings()

    def __call__(self, files, hana):
        html_re = re.compile(r'\.(html|htm)$')

        # Local cache to avoid multiple lookups
        url_endpoint_cache = {}

        for filename, hfile in files:
            if not html_re.search(filename):
                continue

            if not hfile['contents']:
                continue

            # If we have cache and file has not changed, move on
            if self.cache.get(filename) == hfile.sha1sum():
                continue

            self.logger.debug('Processing %s', filename)

            mentions = ronkyuu.findMentions(None, content=hfile['contents'], test_urls=False, exclude_domains=self.exclude_domains)

            if not self.webmention_meta_key in hfile:
                hfile[self.webmention_meta_key] = dict()

            for href in mentions['refs']:
                self.logger.debug('Found URL: %s', href)

                wm_url = url_endpoint_cache.get(href)

                if not wm_url:
                    self.logger.debug('Looking up Webmention endpoint for %s', href)
                    wm_status, wm_url = ronkyuu.discoverEndpoint(href, test_urls=False)

                    if wm_status != requests.codes.ok:
                        continue

                    if not wm_url:
                        continue

                    url_endpoint_cache[href] = wm_url

                # Keep only URLs with endpoints
                hfile[self.webmention_meta_key][href] = wm_url
                self.logger.debug('Found webmention endpoint "%s" for "%s"', wm_url, href)

            if self.cache_file:
                self.cache[filename] = hfile.sha1sum()

        if self.cache_file:
            with open(self.cache_file, 'w') as fp:
                json.dump(self.cache, fp)

class SendWebmentions(object):
    def __init__(self, base_uri, webmention_meta_key=WEBMENTION_META_KEY, allow_insecure_https=False):
        self.logger = logging.getLogger('{}.{}'.format(self.__module__, self.__class__.__name__))

        self.base_uri = base_uri
        self.webmention_meta_key = webmention_meta_key

        parts = urlparse.urlparse(base_uri)

        if allow_insecure_https:
            urllib3.disable_warnings()

    def __call__(self, files, hana):
        html_re = re.compile(r'\.(html|htm)$')

        for filename, hfile in files:
            # If there are no URLs or endpoints detected, move on
            if not self.webmention_meta_key in hfile:
                continue

            source_url = urlparse.urljoin(self.base_uri, filename)

            for href, wm_url in hfile[self.webmention_meta_key].iteritems():
                if not wm_url:
                    continue

                self.logger.debug('Sending webmention for "%s" to endpoint "%s" for "%s"', filename, wm_url, href)

                status_code = ronkyuu.sendWebmention(source_url, href, wm_url)
                status_code = requests.codes.ok

                if status_code == requests.codes.ok:
                    self.logger.info('Webmention sent successfully for %s', href)
                else:
                    self.logger.info('Webmention send for "%s" returned a status code of %s', href, status_code)

