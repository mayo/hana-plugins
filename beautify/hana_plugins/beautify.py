from hana.errors import HanaPluginError

#TODO: clean up prints. use logging

from bs4 import BeautifulSoup
import re

#TODO: this screws with html introducing new white space/newlines.

def beautify(indent_size=4, indent_char=" "):
    html_re = re.compile(r'\.(htm|html)$')

    def beautify_plugin(files, hana):
        for filename, f in files:

            if not html_re.search(filename):
                continue

            #TODO temporary
            if not f['contents'][0:2] == '<!':
                continue

            soup = BeautifulSoup(f['contents'], 'html.parser')
            f['contents'] = soup.prettify(formatter="minimal")

    return beautify_plugin

