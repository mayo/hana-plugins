from hana.errors import HanaPluginError
import os
import shutil

# Add static assets to hana files

def assets(assets, base_dir, create_dirs=True):

    def asset_plugin(files, hana):
        for src, dst in assets.items():
            if not dst:
                raise InvalidAssetDefinition(src)

            src = os.path.join(src)
            dst = os.path.join(base_dir, dst)

            if create_dirs:
                def makedirs(path, dir):
                    if not dir:
                        return

                    if os.path.isdir(os.path.join(path, dir)):
                        return

                    makedirs(*os.path.split(path))

                    if os.path.isdir(path) or path == '':
                        dirpath = os.path.join(path, dir)
                        os.mkdir(dirpath)
                        return

                makedirs(*os.path.split(os.path.dirname(dst)))

            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy(src, dst)

    return asset_plugin

class InvalidAssetDefinitionError(HanaPluginError): pass


