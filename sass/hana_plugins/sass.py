from __future__ import absolute_import
from hana.errors import HanaPluginError
import logging
import os
import re

import sass as scss

class Sass(object):

    def __init__(self):
        self.logger = logging.getLogger(self.__module__)

        self.output_extension = ".css"

        self.file_re = re.compile(r'\.(scss|sass)$')


    def __call__(self, files, hana):

        #TODO: fix this in Hana
        for filename, f in dict(files).items():
            if not self.file_re.search(filename):
                continue

            self.logger.debug('sass {}'.format(filename))

            filebase = os.path.basename(filename)

            if filebase.startswith('_'):
                self.logger.debug('sass ignoring {}'.format(filename))
                hana.files.remove(filename)
                continue

            f['contents'] = scss.compile(
                string=f['contents'].encode('utf-8'),
                output_style='expanded',
            )

            file_basename, _ = os.path.splitext(filename)
            new_name = "{:s}{:s}".format(file_basename, self.output_extension)

            self.logger.debug('renaming %s to %s', filename, new_name)
            hana.files.rename(filename, new_name)


