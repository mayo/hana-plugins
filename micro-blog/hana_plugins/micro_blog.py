from __future__ import absolute_import
import logging
import os
import urllib
from http import client as httplib

from hana.errors import HanaPluginError

def ping(feed_url):
    logger = logging.getLogger(__name__)

    def plugin(hana, files):
        data = urllib.parse.urlencode({'url': feed_url})

        conn = httplib.HTTPSConnection('micro.blog')
        conn.request('POST', '/ping', data)
        response = conn.getresponse()

        logger.info('Sending ping to Micro.blog for {}... {}'.format(feed_url, response.reason))

    return plugin

