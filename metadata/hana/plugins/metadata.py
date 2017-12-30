import logging
# Metadata plugin

#TODO: this should probably become the set_metadata plugin from build.py. This should be handled from initial configuration
def metadata(data):
    logger = logging.getLogger(__name__)

    logger.debug('loading metadata')

    def metadata_plugin(files, hana):
        hana.metadata.update(data)

    return metadata_plugin


