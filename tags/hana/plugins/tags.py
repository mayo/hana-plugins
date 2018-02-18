from hana.errors import HanaPluginError
import pathspec

# TODO: consider splitting prev/next to a 'navigation' plugin, rather than here. Leave this to only
#       deal with tags.
#
class Tags():
    def __init__(self, config={}, metadata_key='tags', default_tag=None, previous_key='previous', next_key='next'):
        # default_denotes which collection is default and applied to the actual files. Unless
        # articles in each collection are generated dynamically or in separate files, there can
        # only be one real collection, and the default one is it.

        #TODO: validate config input. can't start with _
        self.config = config
        self.metadata_key = metadata_key
        self.default_tag = default_tag
        self.previous_key = previous_key
        self.next_key = next_key

        # Initialize empty tags
        self.tags = {}
        self.patterns = {}

        # Generate patterns
        for tag, tag_def in self.config.iteritems():
            if 'pattern' in tag_def:
                patterns = tag_def['pattern']

                if isinstance(patterns, basestring):
                    patterns = [patterns]

                self.patterns[tag] = pathspec.PathSpec.from_lines('gitwildmatch', patterns)

                #Initialize tags for all the patterns
                if tag not in self.tags:
                    self.tags[tag] = {}

    def __call__(self, files, hana):

        for filename, f in files:
            #TODO: this should probably be taken care of globally
            f['path'] = filename

            # Add tags metadata
            if not self.metadata_key in f:
                f[self.metadata_key] = []

            # Add pattern tags
            for tag, tag_pat in self.patterns.iteritems():
                if tag_pat.match_file(filename):
                    f[self.metadata_key].append(tag)

            # Make set and grab the tags
            file_tags = set(f[self.metadata_key])
            f[self.metadata_key] = file_tags

            # Enumerate tags and keep track of files
            for tag in file_tags:
                if tag not in self.tags:
                    self.tags[tag] = {}

                # Synthetize the metadata, as we don't want it to update from other plugins
                # TODO: rethink this. We do need content in certain format (transformed, but not
                #       full templates applied), but other metadata should be updated?
                self.tags[tag][filename] = dict(f)


        # Initialize main tag list in hana
        hana.metadata[self.metadata_key] = {}

        for tag, tag_def in self.tags.iteritems():
            tag_def = tag_def.itervalues()

            # Sort
            if tag in self.config and self.config[tag].get('sort_by'):
                sort_key = self.config[tag].get('sort_by')
                tag_def = sorted(tag_def, key=lambda f_meta: f_meta[sort_key])

            # Reverse
            if tag in self.config and self.config[tag].get('reverse', False):
                tag_def = reversed(tag_def)

            # Synthetize a list, as Jinja doesn't seem to be dealing well with iterator here
            # Set prev/next links for primary tag
            coll = []

            # Set prev/next links for tag
            for idx, post in enumerate(tag_def):
                coll.append(post)

                if idx < 1:
                    continue

                prev_post = coll[idx-1]
                curr_post = coll[idx]

                #next_item = {'path': post['path'], 'title': post.get('title')}
                #prev_item = {'path': prev_post['path'], 'title': prev_post.get('title')}

                # set it within tag
                prev_post[self.next_key] = curr_post
                coll[idx][self.previous_key] = prev_post

                if tag == self.default_tag:
                    # Set prev/next on the default tag. This is necessary for the global blog
                    # prev/next to work.
                    hana.files[prev_post['path']][self.next_key] = curr_post
                    hana.files[post['path']][self.previous_key] = prev_post

            hana.metadata[self.metadata_key][tag] = coll

