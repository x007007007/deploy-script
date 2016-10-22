import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from fabric.api import *
from fabric.contrib import files
from deploy_utils import instance_template



def deploy_base():
    sudo("apt-get install -y vim python python3 virtualenv ")


def deploy_home_pycommon(supervisor_admin_port=None, pip_port=83141):
    """

    :param supervisor_admin_port: supervisor admin port default is localhost:9001
    :return:
    """
    if supervisor_admin_port is None:
        supervisor_admin_port = 'localhost:9001'

    run("mkdir -p ~/.config/supervisord/")

    with hide('warnings', 'running', 'stdout', 'stderr'):
        home = run("echo $HOME")
        user = run("whoami")


    if not files.exists("~/.virtualenvs/common2"):
        run("mkdir -p ~/.virtualenvs/")
        run("virtualenv -p `which python2` ~/.virtualenvs/common2")

    if not files.exists("~/.virtualenvs/common3"):
        run("mkdir -p ~/.virtualenvs/")
        run("virtualenv -p `which python3` ~/.virtualenvs/common3")
    with prefix("source {home}/.virtualenvs/common2/bin/activate".format(home=home)):
        run("pip install --upgrade pip")
        run("pip install --upgrade supervisor")
        run("pip install --upgrade virtualenv")
        run("pip install --upgrade devpi-server")
        run("pip install --upgrade devpi-web")

        with instance_template("./conf/supervisord.conf", HOME=home, admin_addr=supervisor_admin_port) as tpl:
            put(tpl, "~/.config/supervisord/supervisord.conf")

        with hide('warnings', 'running', 'stdout', 'stderr'):
            cmd = run("which devpi-server")

        with instance_template(
            "./conf/supervisord.conf.d/devpi_server.conf",
            CMD=cmd,
            SERVER_DIR="/.virtualenvs/tmp",
            USER=user,
            port=pip_port
        ) as tpl:
            run("mkdir -p ~/.config/supervisord/supervisord.conf.d")
            put(tpl, "~/.config/supervisord/supervisord.conf.d/")

        try:
            sudo("supervisorctl reload -c {home}/.config/supervisord/supervisord.conf".format(home=home))
        except:
            sudo("supervisord -c {home}/.config/supervisord/supervisord.conf".format(home=home))

        with instance_template("./conf/pip/pip.conf", port=pip_port) as tpl:
            run("mkdir ~/.pip")
            put(tpl, "~/.pip/pip.conf")

        with instance_template("./conf/pydistutils.cfg", port=pip_port) as tpl:
            put(tpl, "~/.pydistutils.cfg")