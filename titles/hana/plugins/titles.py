from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from hana.errors import HanaPluginError
import re

#TODO: fix
def titles(remove=False):
    md_re = re.compile(r'\.(md|markdown)$')
    html_re = re.compile(r'\.(html|htm)$')

    md_pattern = re.compile(r'^\s*#\s*([^n]+?) *#* *(?:\n+|$)')

    def title_plugin(files, hana):
        for filename, f in files:
            if 'title' in f:
                continue

            title = None

            if md_re.search(filename):
                #FIXME - doesn't do anything with the match
                match = md_pattern.match(f['contents'])

            if html_re.search(filename):
                h1_tags = SoupStrainer('h1')
                soup = BeautifulSoup(f['contents'], 'html.parser', parse_only=p_tags)

                title = h1.string.strip()

            if not title:
                continue

            f['title'] = title

            if remove:
                #TODO: remove title from contents
                pass

    return title_plugin

