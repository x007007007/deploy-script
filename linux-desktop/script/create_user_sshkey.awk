#!/usr/bin/awk -f
BEGIN{
    FS = ":";
}
{
    username=$1;
    uid=$3;
    gid=$4;
    homepath=$6;
    if( $6 ~ /\/home\/.*/ ) {
        print $1, $6;
        system(sprintf("mkdir -p %s/.ssh/login", homepath));
        system(sprintf("ssh-keygen -b4096 -t rsa -N \"\" -C\"autologin for %s `date +\"%%F %%H:%%m:%%S\"`\" -f %s/.ssh/login/auto",$1, homepath)); \
        system(sprintf("cp -f %s/.ssh/login/auto /tmp/key/%s_login.prv", homepath, username));
        system(sprintf("cat %s/.ssh/login/*.pub > %s/.ssh/authorized_keys", homepath, homepath));
        system(sprintf("chown %s:%s -R %s/.ssh", uid, gid, homepath));
    }
}