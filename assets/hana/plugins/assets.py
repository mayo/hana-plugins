import os
import logging
import shutil

from hana.core import FSFile
from hana.errors import HanaPluginError

# Add static assets to hana files

def assets(assets, base_dir='', create_dirs=True, sideload=False):
    logger = logging.getLogger(__name__)

    def asset_load(files, hana):
        for src, dst in assets.items():
            if not dst:
                raise InvalidAssetDefinition(src)

            dst = os.path.join(base_dir, dst)

            if dst in files:
                raise FileExistsError("File {} already exists".format(dst))

            if os.path.isdir(src):
                for path, _, sfiles in os.walk(src):
                    sub_path = path[len(src):]

                    for sfile in sfiles:
                        src_path = os.path.join(path, sfile)
                        dst_path = os.path.join(dst, sub_path, sfile)

                        files.add(dst_path, FSFile(src_path))

            else:
                files.add(dst, FSFile(src))

    def asset_sideload(files, hana):
        for src, dst in assets.items():
            if not dst:
                raise InvalidAssetDefinition(src)

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

    if sideload:
        return asset_sideload

    return asset_load

class AssetPluginError(HanaPluginError):
    pass

class InvalidAssetDefinitionError(AssetPluginError):
    pass

class FileExistsError(AssetPluginError):
    pass

