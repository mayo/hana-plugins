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
                    'left-single-quote': '&sbquo;', # sb is not a typo!
                    'right-single-quote': '&lsquo;',
                    'left-double-quote': '&bdquo;',
                    'right-double-quote': '&ldquo;'
                }
            }
        }

        self.md = markdown.Markdown(
                extensions=extensions,
                extension_configs=extension_configs,
                output_format='html5'
        )


    def __call__(self, files, hana):
        md_re = re.compile(r'\.(md|markdown)$')

        for filename, f in files:
            if not md_re.search(filename):
                continue

            self.logger.debug('markdown {}'.format(filename))

            file_basename, _ = os.path.splitext(filename)
            new_name = "{:s}{:s}".format(file_basename, self.output_extension)

            files.rename(filename, new_name)

            f['contents'] = self.md.convert(f['contents'])

