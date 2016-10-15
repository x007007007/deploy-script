import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from fabric.api import *
from fabric.contrib import files
from deploy_utils import instance_template


def deploy_base():
    sudo("apt-get install -y vim python python3 virtualenv ")


def deploy_supervisord(admin_addr=None):
    """

    :param admin_addr:
    :return:
    """
    if admin_addr is None:
        admin_addr = 'localhost:9001'

    run("mkdir -p ~/.config/supervisord/")

    with hide('warnings', 'running', 'stdout', 'stderr'):
        home = run("echo $HOME")

    with instance_template("./conf/supervisord.conf", HOME=home, admin_addr=admin_addr) as tpl:
        put(tpl, "~/.config/supervisord/supervisord.conf")

    if not files.exists("~/.virtualenvs/supervisord"):
        run("mkdir -p ~/.virtualenvs/")
        run("virtualenv -p `which python2` ~/.virtualenvs/supervisord")
    with prefix("source {home}/.virtualenvs/supervisord/bin/activate".format(home=home)):
        run("pip install --upgrade pip")
        run("pip install --upgrade supervisor")
        try:
            sudo("{home}/.virtualenvs/supervisord/bin/supervisorctl reload -c {home}/.config/supervisord/supervisord.conf".format(home=home))
        except:
            sudo("{home}/.virtualenvs/supervisord/bin/supervisord -c {home}/.config/supervisord/supervisord.conf".format(home=home))

