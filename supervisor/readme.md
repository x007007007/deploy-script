=deploy supervisor in user home=

`fab deploy_base -H host -u user`

`fab deploy_home_pycommon:admin_addr="*:9001" -H hostaddr -u username` 
deploy python common server include:

    1. supervisor
    2. devpi