
# Metadata plugin

#TODO: this should probably become the set_metadata plugin from build.py. This should be handled from initial configuration
def metadata(metadata):
    print 'loading metadata'
    def metadata_plugin(files, hana):
        hana.metadata.update(metadata)

    return metadata_plugin


