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
        url_endpoints = {}

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

            for href in mentions['refs']:
                self.logger.debug('Found URL: %s', href)

                wm_url = url_endpoints.get(href, False)

                if wm_url == False:
                    self.logger.debug('Looking up Webmention endpoint for %s', href)
                    wm_status, wm_url = ronkyuu.discoverEndpoint(href, test_urls=False)

                    if wm_status != requests.codes.ok:
                        continue

                    url_endpoints[href] = wm_url

            # Keep only URLs with endpoints
            hfile[self.webmention_meta_key] = {href: ep for href, ep in url_endpoints.iteritems() if ep}

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

                status_code = ronkyuu.sendWebmention(source_url, href, wm_url)
                status_code = requests.codes.ok

                if status_code == requests.codes.ok:
                    self.logger.debug('Webmention sent successfully')
                else:
                    self.logger.debug('Webmention send returned a status code of %s', status_code)

