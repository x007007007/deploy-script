# -*- coding:utf-8 -*-
"""
桌面自动部署  debian
"""

from fabric.api import *
from fabric.colors import green, red
from fabfile_base import install, config, FabricException, read_info




env.password = "xxc"




def deploy_base():
    install(['sudo', 'vim', 'zip'])
    config('config/vim.conf', '/etc/vim/vimrc')
    config('config/ssh/ssh_config', '/etc/ssh/')
    sudo('mkdir -p /etc/bashrc.d/')
    config('config/bashrc.d/prompt.sh', '/etc/bashrc.d/')
    put("config/bashrc_init.inject", "/tmp/")
    sudo("grep A3BE697D-5DC6-4D06-A24D-64C796B6677C /etc/bash.bashrc "
         "|| cat /tmp/bashrc_init.inject >> /etc/bash.bashrc "
         "&& echo inject bashrc loader!!!")
    deploy_script()


def deploy_script():
    sudo("mkdir -p /opt/scripts/")
    run("mkdir -p /tmp/scripts")
    put("script/*", "/tmp/scripts")
    sudo("mv /tmp/scripts/* /opt/scripts/")
    sudo("chown root:root -R /opt/scripts")
    sudo("chmod 755 -R /opt/scripts")
    sudo("rm -rf /tmp/scripts")


def deploy_ssh(refresh_key=False):
    deploy_base_user_ssh()
    sudo("mkdir -p /etc/ssh/key/")
    sudo("chmod 755 /etc/ssh/key")
    run("mkdir -p /tmp/config/")

    sudo("cp /etc/ssh/ssh_host_{rsa,dsa,ecdsa,ed25519}_key*] /etc/ssh/key/ ||echo do not find")

    if refresh_key:
        sudo('rm -f /etc/ssh/key/*')
        sudo('yes y|ssh-keygen -b 4096 -t rsa -N "" -f /etc/ssh/key/ssh_host_rsa_key')
        sudo('yes y|ssh-keygen -t dsa -N "" -f /etc/ssh/key/ssh_host_dsa_key')
        sudo('yes y|ssh-keygen -b521 -t ecdsa  -N "" -f /etc/ssh/key/ssh_host_ecdsa_key')
        sudo('yes y|ssh-keygen -b 9192 -t ed25519 -N "" -f /etc/ssh/key/ssh_host_ed25519_key')

    config("config/ssh/sshd_config", "/etc/ssh/sshd_config")
    sudo("service ssh restart")
    sudo('rm -f /etc/ssh/ssh_host_{rsa,dsa,ecdsa,ed25519}_key*]')


def deploy_base_user_ssh(renew=False):
    sudo("mkdir -p /tmp/key/")
    sudo("rm -rf /tmp/key/*")
    sudo(r"""/opt/scripts/create_user_sshkey.awk /etc/passwd""")
    print read_info
    password = read_info("zip密码:")
    if len(password) > 0:
        sudo('zip -rjXP"{}" /tmp/key.zip /tmp/key'.format(password))
    else:
        sudo('zip -rjX /tmp/key.zip /tmp/key')
    get("/tmp/key.zip")
    sudo("rm -rf /tmp/key /tmp/key.zip")


def deploy_python():
    install(['python-pip'])
