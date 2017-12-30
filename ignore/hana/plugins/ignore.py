from hana.errors import HanaPluginError
import pathspec
#TODO: clean up prints. use logging

def ignore(patterns):
    spec = pathspec.PathSpec.from_lines('gitwildmatch', patterns)

    def ignore_plugin(files, hana):
        matches = spec.match_files(files.filenames())

        for f in matches:
            print 'ignore ', f
            files.remove(f)

    return ignore_plugin

