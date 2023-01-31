from __future__ import absolute_import
from hana.errors import HanaPluginError
import logging
import markdown
from mdfigure import FigureExtension
import os
import re

class Markdown(object):

    def __init__(self, extension='.html', img_figure=False):
        self.logger = logging.getLogger(self.__module__)

        self.output_extension = extension

        extensions = [
            'markdown.extensions.smarty',
        ]

        if img_figure:
            extensions.append(FigureExtension())

        extension_configs = {
            'markdown.extensions.smarty': {
                'substitutions': {
                    'left-single-quote': '&lsquo;', # sb is not a typo!
                    'right-single-quote': '&rsquo;',
                    'left-double-quote': '&ldquo;',
                    'right-double-quote': '&rdquo;'
                }
            }
        }

        self.md = markdown.Markdown(
                extensions=extensions,
                extension_configs=extension_configs,
                output_format='html5'
        )

        self.md_re = re.compile(r'\.(md|markdown)$')


    def __call__(self, files, hana):

        #TODO: fix this in Hana
        for filename, f in dict(files).items():
            if not self.md_re.search(filename):
                continue

            self.logger.debug('markdown {}'.format(filename))

            file_basename, _ = os.path.splitext(filename)
            new_name = "{:s}{:s}".format(file_basename, self.output_extension)

            self.logger.debug('renaming %s to %s', filename, new_name)
            hana.files.rename(filename, new_name)

            f['contents'] = self.md.convert(f['contents'])
            self.md.reset()
