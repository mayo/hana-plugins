from hana.errors import HanaPluginError
import os
import re

#TODO: clean up prints. use logging

class PrettyUrl():

    def __init__(self, relative=True, index_file='index.html'):
        self.index_file = index_file

    def __call__(self, files, hana):
        html_re = re.compile(r'\.(htm|html)$')

        for filename, f in files:
            if not html_re.search(filename):
                continue

            if not f.get('permalink', True):
                continue

            path, _ = os.path.splitext(filename)
            path = os.path.join(path, self.index_file)
            #print path

            files.rename(filename, path)
            #TODO: Is this supposed to be attribute or metadata?
            f.permalink = True

