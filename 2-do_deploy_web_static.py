#!/usr/bin/python3
# fabric script to deploy web_static to servers

from fabric.api import env, run, put
import os

env.hosts = ['107.23.102.134', '18.210.17.11']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/deploy_airbnb'

def do_deploy(archive_path):
    "distributes an archive to your web servers, using the function"
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')

        # extract filename
        name = archive_path.split('/')[-1]
        name_not_exist = name.split('.')[0]

        # create directory
        path = '/data/web_static/releases/{}'.format(name_not_exist)
        run('mkdir -p {}'.format(path))

        # decompress archive
        run('tar -xzf /tmp/{} -C {}'.format(name, path))
        print("Successfully Decompressed the archive YAYAAY")

        # delete archive
        run('rm /tmp/{}'.format(name))
        run('mv {}web_static/* {}'.format(path, path))

        # delete symbolic link
        run('rm -rf {}web_static'.format(path))
        run('rm -rf /data/web_static/current')

        # create new symbolic link
        run("ln -s {} /data/web_static/current".format(path))

        print("Deployment Successfully")
        return True
    except Exception as e:
        print("Failed!!!")
        return False
