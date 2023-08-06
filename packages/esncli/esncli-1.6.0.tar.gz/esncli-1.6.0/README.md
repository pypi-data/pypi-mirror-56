openpaas-esncli
==================

usage: esncli [--config-file CONFIG_FILE] [-v] [--version] [-h] [-d] -l LOGIN
              -p PASSWORD --url URL [--host HOST] [--no-verify]
              {password,core-login,core-features,core-dav,core-email,core-web,inbox,contact,calendar,lemonldap,james,linshare,general,core-ldap,autoconf,whoami,domain-create}
              ...

Description of program init.esn.config.py.

positional arguments:
  {password,core-login,core-features,core-dav,core-email,core-web,inbox,contact,calendar,lemonldap,james,linshare,general,core-ldap,autoconf,whoami,domain-create}
    password            Description of password
    core-login          Description of core-login
    core-features       Description of core-features
    core-dav            Description of core-dav
    core-email          Description of core-email
    core-web            Description of core-web
    inbox               Description of inbox
    contact             Description of contact
    calendar            Description of calendar
    lemonldap           Description of lemonldap
    james               Description of james
    linshare            Description of linshare
    general             Description of general
    core-ldap           Description of core-ldap
    autoconf            Description of autoconf
    whoami              Description of autoconf
    domain-create       Create a domain in ESN

optional arguments:
  --config-file CONFIG_FILE
                        Other configuration file.
  -v, --verbose
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -d                    debug level : default : 0.
  -l LOGIN, --login LOGIN
                        Email of an administrator. You can set an env variable
                        ESN_CLI_LOGIN instead of this parameter.
  -p PASSWORD, --password PASSWORD
                        Password of the administrator. You can set an env
                        variable ESN_CLI_PASSWORD instead of this parameter.
  --url URL             Base url of esn like https://192.168.1.1. You can set
                        an env variable ESN_CLI_URL instead of this parameter.
  --host HOST           Vhost name to override IP if needed. ex 'op-
                        admin.openpaas.org'. You can set an env variable
                        ESN_CLI_HOST instead of this parameter.
  --no-verify           Do not verify SSL certificate