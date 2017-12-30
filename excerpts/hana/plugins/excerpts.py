from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import pathspec

def excerpts(files, hana):
    match = pathspec.PathSpec.from_lines('gitwildmatch', ['*.htm', '*.html']).match_file

    for filename, f in files:
        if not match(filename):
            continue

        if f.get('excerpt'):
            continue

        p_tags = SoupStrainer('p')
        soup = BeautifulSoup(f['contents'], 'html.parser', parse_only=p_tags)

        p = soup.p

        while p and p.img:
            p = p.next_sibling

        f['excerpt'] = p


