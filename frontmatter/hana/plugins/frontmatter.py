from __future__ import absolute_import
import logging

import frontmatter as fm

def frontmatter(files, hana):
    logger = logging.getLogger(__name__)

    for filename, f in files:
        if f.is_binary:
            continue

        # This will strip empty front matter statement
        metadata, f['contents'] = fm.parse(f['contents'])

        logger.debug('frontmatter %s', filename)

        if metadata:
            f.update(metadata)

