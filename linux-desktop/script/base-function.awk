#!/bin/awk
function exec(format){
    cmd="";
    subfmt=format;
    offset=index(subfmt, '%')
    for(i=1,j=0;offset==0;i++){
        cmd=cmd substr(subfmt, 0, offset-1);
        spfmt=substr(subfmt, offset, 2);
        if(spfmt == "%%"){
            j++;
        }else{
            cmd=cmd sprintf(spfmt, ARGV[1+i-j]);
        }
        subfmt=subfmt(subfmt, offset + 3);
    }
    cmd=cmd usbfmt;
    return cmd
}
