#!/usr/bin/python
import pexpect
import re


def IMGDEL(ip,username='admin',password='Cisco12345'):
        syntax="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "+username+"@"+ip
        login=pexpect.spawn (syntax)
        login.expect("[P|p]assword:", timeout=180)
        login.sendline(password)
        login.expect('#',timeout=60)
        login.sendline('terminal len 0')
        login.expect('#')
        print login.before
        login.sendline('config t')
        login.expect('#')
        login.sendline('feature bash')
        login.expect('#')
        login.sendline('run bash')
        login.expect('$')
        login.sendline('rm -rf /bootflash/*.bin')
        login.expect('$')
        login.sendline('rm -rf /bootflash/*.cco')
        login.expect('$')
        print "ssh module success:"
        return login
