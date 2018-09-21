#/usr/bin/
import pexpect
import re

def SSH(ip,username,password,hostname,program='NONE'):
  syntax="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "+username+"@"+ip
  check='{}.*#|.*$'.format(hostname)
  try:
    login=pexpect.spawn (syntax)
    login.expect("[P|p]assword:", timeout=180)
    login.sendline(password)
    login.expect(check,timeout=60)
    login.sendline('terminal len 0')
    login.expect(check)
    print login.before
    print "ssh module success:"
    return login


  except:
    print "{} - Problem using ssh to: {}".format(program,ip)
    print login.before
    return "ERROR"

