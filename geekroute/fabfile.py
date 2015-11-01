# -*- coding:utf-8 -*-
"""
OpenWrt自动安装
"""

from fabric.api import *
from fabric.colors import green, red


env.shell = "/bin/sh -c"

env.roledefs = {
    'openwrt': ['root@192.168.30:21212',],
    'tplink': ['admin@192.168.18:20', ]
}

"""
luci-i18n-ahcp-zh-cn
luci-i18n-asterisk-zh-cn
luci-i18n-base-zh-cn
luci-i18n-commands-zh-cn
luci-i18n-ddns-zh-cn
luci-i18n-diag-core-zh-cn
luci-i18n-diag-devinfo-zh-cn
luci-i18n-firewall-zh-cn
luci-i18n-freifunk-policyrouting-zh-cn
luci-i18n-freifunk-zh-cn
luci-i18n-hd-idle-zh-cn
luci-i18n-meshwizard-zh-cn
luci-i18n-minidlna-zh-cn
luci-i18n-mmc-over-gpio-zh-cn
luci-i18n-multiwan-zh-cn
luci-i18n-ntpc-zh-cn
luci-i18n-olsr-zh-cn
luci-i18n-openvpn-zh-cn
luci-i18n-p2pblock-zh-cn
luci-i18n-p910nd-zh-cn
luci-i18n-pbx-voicemail-zh-cn
luci-i18n-pbx-zh-cn
luci-i18n-polipo-zh-cn
luci-i18n-privoxy-zh-cn
luci-i18n-qos-zh-cn
luci-i18n-radvd-zh-cn
luci-i18n-samba-zh-cn
luci-i18n-splash-zh-cn
luci-i18n-statistics-zh-cn
luci-i18n-tinyproxy-zh-cn
luci-i18n-transmission-zh-cn
luci-i18n-upnp-zh-cn
luci-i18n-vnstat-zh-cn
luci-i18n-voice-core-zh-cn
luci-i18n-voice-diag-zh-cn
luci-i18n-watchcat-zh-cn
luci-i18n-wol-zh-cn
luci-i18n-wshaper-zh-cn
"""
class FabricException(Exception):
    pass

def install(name, retry_time=0):
    try:
        print(green("install {}".format(name)))
        run('opkg install {}'.format(name))
    except FabricException, e:
        print(red(e.message), e)
        run('opkg update')
        if retry_time < 3:
            print(green("retry {}".format(retry_time)))
            install(name, retry_time=retry_time+1)


def pip_install(name, retry_time=0):
    try:
        print(green("install {}".format(name)))
        run("pip install --upgrade {}".format(name))
    except FabricException, e:
        print(red(e.message), e)
        if retry_time < 3:
            print(green("retry {}".format(retry_time)))
            pip_install(name, retry_time+1)



def deploy():
    for pkg in ['luci-ssl', 'luci-app-privoxy', 'luci-app-qos', 'luci-app-upnp', 'luci-app-samba',
                'luci-app-transmission', 'luci-app-wol']:
        install(pkg)

    for pkg in ['luci-i18n-base-zh-cn', 'luci-i18n-privoxy-zh-cn', 'luci-i18n-qos-zh-cn', 'luci-i18n-upnp-zh-cn',
                'luci-i18n-samba-zh-cn', 'luci-i18n-watchcat-zh-cn', 'luci-i18n-wol-zh-cn']:
        install(pkg)

    run('/etc/init.d/uhttpd restart')

    for pkg in ['python', 'python-pip']:
        install(pkg)

    for pip_pkg in ['pip', 'virtualenv', 'shadowsocks']:
        pip_install(pip_pkg)
