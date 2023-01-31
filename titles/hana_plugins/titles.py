import logging
import re

from bs4 import BeautifulSoup
from bs4 import SoupStrainer

from hana.errors import HanaPluginError

#TODO: fix
def titles(remove=False):
    logger = logging.getLogger(__name__)

    md_re = re.compile(r'\.(md|markdown)$')
    html_re = re.compile(r'\.(html|htm)$')

    # This should match any first heading in the document
    #TODO: what about the underline style headings?
    md_pattern = re.compile(r'(^\s*#\s*([^n]+?)\s*#*\s*(?:\n+|$))')

    def title_plugin(files, hana):
        for filename, f in files:
            if 'title' in f:
                continue

            title = None
            logger.debug('titles %s', filename)

            if md_re.search(filename):
                #FIXME - doesn't do anything with the match
                match = md_pattern.match(f['contents'])

                if match:
                    pass


            if html_re.search(filename):
                h1_tags = SoupStrainer('h1')
                match = BeautifulSoup(f['contents'], 'html.parser', parse_only=h1_tags)

                if match.string:
                    title = match.string.strip()

            if not title:
                continue

            f['title'] = title

            if remove:
                #TODO: remove title from contents
                pass

    return title_plugin

