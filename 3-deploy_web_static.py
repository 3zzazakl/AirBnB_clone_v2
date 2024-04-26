#!/usr/bin/python3
# fabric script to deploy web_static to servers

from fabric.api import local, env, run, put
from datetime import datetime
import os

env.hosts = ['107.23.102.134', '18.210.17.11']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/deploy_airbnb'


def do_pack():
    """generates a .tgz archive from the contents of the web_static folder"""
    try:
        if not os.path.exists('versions'):
            os.makedirs('versions')
        date = datetime.now().strftime('%Y%m%d%H%M%S')
        file = 'versions/web_static_{}.tgz'.format(date)
        result = local('tar -cvzf {} web_static'.format(file))
        if result.succeeded:
            return file
    except Exception as e:
        return None


def do_deploy(archive_path):
    "distributes an archive to your web servers, using the function"
    if not os.path.exists(archive_path):
        return False
    try:
        archive_file = archive_path[9:]
        n_archive = "/data/web_static/releases/" + archive_file[:-4]
        archived_file = "/tmp/" + archive_file
        put(archive_path, "/tmp/")
        run('sudo mkdir -p {}'.format(n_archive))
        run('sudo tar -xzf {} -C {}'.format(archived_file, n_archive))

        run('sudo rm {}'.format(archived_file))
        run('sudo mv {}/web_static/* {}'.format(n_archive, n_archive))
        run('sudo rm -rf {}/web_static'.format(n_archive))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {} /data/web_static/current'.format(n_archive))

        print("Deployment Successfully")
        return True
    except Exception as e:
        print("Failed!!!")
        return False


def deploy():
    """deploy web_static to web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
