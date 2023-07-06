#!/usr/bin/python3
"""Module to Compress files"""
import os
from datetime import datetime
from fabric.api import local, runs_once


def do_pack():
    """Create a .tgz archive from the contents of the web_static folder."""
    try:
        if not os.path.exists("versions"):
            print("Creating versions directory")
            os.mkdir("versions")

        now = datetime.now()
        archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second
        )
        archive_path = "versions/{}".format(archive_name)
        archive_command = "tar -czvf {} web_static".format(archive_path)

        print("Packing web_static to: {}".format(archive_path))
        local(archive_command)

        if os.path.exists(archive_path):
            print("Archive created successfully: {}".format(archive_path))
            return archive_path
        else:
            print("Failed to create archive.")
            return None

    except Exception as e:
        print("Error occurred during archive creation:", str(e))
        return None
