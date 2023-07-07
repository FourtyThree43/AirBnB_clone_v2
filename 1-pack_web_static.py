#!/usr/bin/python3
"""Module to Compress files"""
import os
from datetime import datetime
from fabric.api import local


def do_pack():
    """Create a .tgz archive from the contents of the web_static folder."""
    if not os.path.exists("versions"):
        print("Creating versions directory")
        os.mkdir("versions")

    now = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(now)
    archive_path = "versions/{}".format(archive_name)

    print("Packing web_static to: {}".format(archive_path))
    archive_command = local("tar -czvf {} web_static".format(archive_path))

    if archive_command.succeeded:
        print("Archive created successfully: {}".format(archive_path))
        return archive_path
    else:
        print("Failed to create archive.")
        return None
