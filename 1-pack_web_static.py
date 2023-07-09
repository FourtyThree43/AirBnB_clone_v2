#!/usr/bin/python3
"""Module to Compress files"""
import os
from datetime import datetime
from fabric.api import local


def do_pack():
    """Create a .tgz archive from the contents of the web_static folder."""

    local("mkdir -p versions")

    now = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(now)
    archive_path = "versions/{}".format(archive_name)

    print("Packing web_static to {}".format(archive_path))
    archive = local("tar -cvzf {} web_static".format(archive_path))
    size = os.stat(archive_path).st_size
    print("web_static packed: {} -> {}Bytes".format(archive_path, size))

    if archive.succeeded:
        return archive_path
    else:
        return None
