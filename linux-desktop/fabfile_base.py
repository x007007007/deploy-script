# -*- coding:utf-8 -*-
import sys
if sys.version_info.major < 3:
    read_info = raw_input
else:
    read_info = input

from fabric.api import *
from fabric.colors import green, red


def config(lp, rp):
    sudo("rm -rf /tmp/conf")
    run("mkdir -p /tmp/conf/")
    put(lp, "/tmp/conf/conf")
    sudo('chown root:root /tmp/conf/conf')
    sudo("mv -f /tmp/conf/conf '{}'".format(rp))


def install(names, su=True):
    if isinstance(names, (tuple, list, set)):
        names = " ".join(list(names))
    print(green("install {}".format(names)))
    sudo("apt-get install --fix-missing {}".format(names))


class FabricException(Exception): pass