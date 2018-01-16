from __future__ import absolute_import
import logging

import frontmatter as fm

def frontmatter(files, hana):
    logger = logging.getLogger(__name__)

    for filename, f in files:
        if f.is_binary:
            continue

        logger.debug('frontmatter %s', filename)

        # This will strip empty front matter statement
        metadata, f['contents'] = fm.parse(f['contents'])


        if metadata:
            f.update(metadata)

