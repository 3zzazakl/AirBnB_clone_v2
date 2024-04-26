#!/usr/bin/python3
"""
Fabric script (based on the file 100-clean_web_static.py)
"""

import os
from fabric.api import *

env.hosts = ['107.23.102.134', '18.210.17.11']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/deploy_airbnb'


def do_clean():
    """
    Deletes out-of-date archives,
    creates a new archive, and deploys it to your web servers.
    """
    num = 1 if int(num) == 0 else int(num)
    archives = sorted(os.listdir('versions'))
    [archives.pop() for i in range(num)]
    with lcd('versions'):
        [local('rm {}'.format(archive)) for archive in archives]

    with cd('/data/web_static/releases'):
        archives = run("ls -tr").split()
        archives = [a for a in archives if a.endswith('.tgz')]
        archives = archives[:num] if num < len(archives) else []
        [run('rm {}'.format(archive)) for archive in archives]
