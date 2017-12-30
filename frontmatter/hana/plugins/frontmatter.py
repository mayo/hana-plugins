from __future__ import absolute_import
import frontmatter as fm

def frontmatter(files, hana):

    for _, f in files:
        if f.is_binary:
            continue

        # This will strip empty front matter statement
        metadata, f['contents'] = fm.parse(f['contents'])

        if metadata:
            f.update(metadata)

