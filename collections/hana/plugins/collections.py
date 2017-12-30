from hana.errors import HanaPluginError

#TODO: clean up prints. use logging



import pathspec

#TODO: define article previous/next links
class Collections():
    KEY = 'collection'

    def __init__(self, config={}):
        #TODO: validate config input. can't start with _
        self.config = config

        # Initialize empty collections
        self.collections = {}
        self.patterns = {}

        for c_name, c_def in self.config.iteritems():
            if 'pattern' in c_def:
                pats = c_def['pattern']

                if isinstance(pats, str):
                    pats = [pats]

                self.patterns[c_name] = pathspec.PathSpec.from_lines('gitwildmatch', pats)

    def __call__(self, files, hana):

        for filename, f in files:
            #print f
            #TODO: this should probably be taken care of globally
            #TODO: metafile experiment
            f['path'] = filename

            # If file has collections defined
            if Collections.KEY in f:
                # Use set to enforce uniqueness
                file_collections = set(f.get(Collections.KEY))

                # Enumerate collections and keep track of files
                for col in file_collections:
                    if col not in self.collections:
                        self.collections[col] = {}

                    self.collections[col][filename] = f

            # Collections definition
            for c_name, c_pat in self.patterns.iteritems():
                if c_pat.match_file(filename):
                    if c_name not in self.collections:
                        self.collections[c_name] = {}

                    # Synthetize the metadata, as we don't want it to update from other plugins
                    self.collections[c_name][filename] = dict(f)


        hana.metadata['collections'] = {}
        for key, collection in self.collections.iteritems():
            collection = collection.itervalues()

            # Sort
            if key in self.config and 'sortBy' in self.config[key]:
                sort_key = self.config[key].get('sortBy')
                collection = sorted(collection, key=lambda f_meta: f_meta[sort_key])

            # Reverse
            if key in self.config and self.config[key].get('reverse', False):
                collection = reversed(collection)

            # Synthetize a list, as Jinja doesn't seem to be dealing well with iterator here
            # Set prev/next links for primary collection
            coll = []

            # Set prev/next links for collection
            for idx, post in enumerate(collection):
                coll.append(post)

                if idx < 1:
                    continue

                next_item = { 'path': post['path'], 'title': post['title'] }
                prev_item = { 'path': coll[idx-1]['path'], 'title': coll[idx-1]['title'] }

                # set it within collection
                coll[idx-1]['next'] = next_item
                coll[idx]['previous'] = prev_item

                # set the default collection as global prev/next
                if key in self.config and self.config[key].get('default', False):
                    files[coll[idx-1]['path']]['next'] = next_item
                    files[post['path']]['previous'] = prev_item


            hana.metadata['collections'][key] = coll


