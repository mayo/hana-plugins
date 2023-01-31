import logging
import os
import re

from hana.errors import HanaPluginError

class PrettyUrl():

    def __init__(self, relative=True, index_file='index.html'):
        self.index_file = index_file
        self.processed_files = []
        self.logger = logging.getLogger(self.__module__)

    def __call__(self, files, hana):
        html_re = re.compile(r'\.(htm|html)$')

        #TODO: fix this in Hana
        for filename, f in dict(files).items():
            if filename in self.processed_files:
                continue

            _, filen = os.path.split(filename)

            if filen == self.index_file:
                self.logger.debug('Ignoring "%s". Already an index file', filename)
                continue

            if not html_re.search(filename):
                continue

            #TODO: what's the meaning of this?
            if not f.get('permalink', True):
                continue

            path, _ = os.path.splitext(filename)
            path = os.path.join(path, self.index_file)

            self.logger.debug('Renaming "%s" to "%s"', filename, path)
            self.processed_files.append(path)
            hana.files.rename(filename, path)

