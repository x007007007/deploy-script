# -*- coding:utf-8 -*-
import sys
if sys.version_info.major < 3:
    read_info = raw_input
else:
    read_info = input

from fabric.api import *
from fabric.colors import green, red


def safe_right(path):
    sudo(r"find {path} -type d -exec chmod 0755 {rep} \;".format(rep='{}', path=path))
    sudo(r"find {path} -type f -exec chmod 0644 {rep} \;".format(rep='{}', path=path))

def config(lp, rp):
    print(green("config:{}".format(rp)))
    sudo("rm -rf /tmp/conf")
    run("mkdir -p /tmp/conf/")
    put(lp, "/tmp/conf/")
    sudo('chown root:root -R /tmp/conf/')
    safe_right('/tmp/conf')
    sudo("mv -f /tmp/conf/* '{}'".format(rp))


def install(names, su=True):
    if isinstance(names, (tuple, list, set)):
        names = " ".join(list(names))
    print(green("install {}".format(names)))
    sudo("apt-get install --fix-missing {}".format(names))


class FabricException(Exception): pass