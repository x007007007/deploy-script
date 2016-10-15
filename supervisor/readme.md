=deploy supervisor in user home

`fab deploy_base -H host -u user`

`fab deploy_supervisord:admin_addr="*:9001" -H host -u user`