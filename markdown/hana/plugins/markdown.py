from __future__ import absolute_import
from hana.errors import HanaPluginError
import markdown
import os
import re

#TODO: clean up prints. use logging

class Markdown(object):

    def __init__(self, config={}):
        #TODO: support file extension pattern

        self.output_extension = config.get('extension', '.html')

        extensions = ['markdown.extensions.smarty']

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
            if 'index.' in filename or 'DS_Store' in filename:
                print 'markdown ', filename

            if not md_re.search(filename):
                continue

            file_basename, _ = os.path.splitext(filename)
            new_name = "{:s}{:s}".format(file_basename, self.output_extension)

            files.rename(filename, new_name)

            f['contents'] = self.md.convert(f['contents'])

