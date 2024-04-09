#!/usr/bin/python3
# fabric script to deploy web_static to servers

from fabric.api import env, run, put
import os

env.hosts = ['107.23.102.134', '18.210.17.11']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school.pem'


def do_deploy(archive_path):
    "distributes an archive to your web servers, using the function"
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')
        archive_name = archive_path.split('/')[-1]
        archive_name_noext = archive_name.split('.')[0]
        run('mkdir -p /data/web_static/releases/{}'.format(archive_name_noext))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.
            format(archive_name, archive_name_noext))
        run('rm /tmp/{}'.format(archive_name))
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/\
            releases/{}/'.format(archive_name_noext, archive_name_noext))
        run('rm -rf /data/web_static/releases/{}/web_static'.
            format(archive_name_noext))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{} /data/web_static/current'.
            format(archive_name_noext))
        return True
    except Exception as e:
        return False
