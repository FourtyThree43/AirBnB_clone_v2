#!/usr/bin/python3
"""Module to Compress files"""
import os
from datetime import datetime
from fabric.api import *

env.hosts = ["54.160.120.200", "54.145.155.255"]
env.user = "ubuntu"


def do_pack():
    """Create a .tgz archive from the contents of the web_static folder."""
    try:
        if not os.path.isdir("versions"):
            os.mkdir("versions")
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = "web_static_{}.tgz".format(now)
        archive_path = "versions/{}".format(archive_name)
        print("Packing web_static to {}".format(archive_path))
        local("tar -cvzf {} web_static".format(archive_path))
        size = os.stat(archive_path).st_size
        print("web_static packed: {} -> {}Bytes".format(archive_path, size))
        return archive_path
    except Exception as e:
        print("Archive creation failed:", str(e))
        return None


def do_deploy(archive_path):
    """Distributes an archive to your web servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")
        filename = os.path.basename(archive_path)
        folder_name = "/data/web_static/releases/{}".format(
                                                      filename.split(".")[0]
                                                    )

        # Uncompress the archive to the folder
        run("mkdir -p {}".format(folder_name))
        run("tar -xzf /tmp/{} -C {}".format(filename, folder_name))
        run("rm /tmp/{}".format(filename))
        run("mv {}/web_static/* {}/".format(folder_name, folder_name))
        run("rm -rf {}/web_static".format(folder_name))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link linked to the new version of the code
        run("ln -s {} /data/web_static/current".format(folder_name))
        print("New version deployed!")

        return True
    except Exception as e:
        print("Deployment failed:", str(e))
        return False


def deploy():
    """Create and distribute an archive to web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
