from hana.errors import HanaPluginError
import logging
import pathspec

def ignore(patterns):
    logger = logging.getLogger(__name__)
    spec = pathspec.PathSpec.from_lines('gitwildmatch', patterns)

    def ignore_plugin(files, hana):
        matches = spec.match_files(hana.files.filenames())

        for f in matches:
            logger.debug('Ignoring {}'.format(f))
            hana.files.remove(f)

    return ignore_plugin

