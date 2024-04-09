#!/usr/bin/python3
# fabric script to generate a tgz of contents

from fabric.api import local
from datetime import datetime
import os


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


if __name__ == "__main__":
    do_pack()
