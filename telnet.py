#/usr/bin/
import sys
import pexpect
import re
import os
import time

def TELNET(ipport,username,password,terms=1):
  syntax1="telnet "+ipport
  ts=re.findall(r'\d+\.\d+\.\d+\.\d+',ipport)
  ts_ip=ts[0]
  print ts_ip
  ts_password='cisco'
  if terms==1:
    ts_port=ipport[-2:]
    print ts_port
    syntax2='telnet '+ts_ip
    cli='clear line '+ts_port
  else:
    syntax2='telnet '+ipport
  terms=int(terms)
  if terms==1:
    try:
      login=pexpect.spawn (syntax2)
      login.expect("[P|p]assword:", timeout=80)
      login.sendline(ts_password)
      time.sleep(1)
      login.expect(">|#|$|",timeout=60)
      login.sendline('terminal len 0')
      login.expect('#|$')
      login.sendline('en')
      login.expect('[P|p]assword:')
      login.sendline(ts_password)
      login.expect("#|$|",timeout=60)
      login.sendline(cli)
      time.sleep(1)
      login.expect('\[confirm\]')
      login.sendline('\n')
      time.sleep(1)
      login.expect('#|$')
      print login.before
      login.sendline(cli)
      time.sleep(1)
      login.expect('\[confirm\]',timeout=60)
      login.sendline('\n')
      time.sleep(1)
      login.expect('#')
      print login.before
      login.close
      log=pexpect.spawn (syntax1)
      log.sendline('\n')
      time.sleep(1)
      check=log.expect(['login:','#'])
      if check==0:
        log.sendline(username)
        log.expect("[P|p]assword:", timeout=180)
        log.sendline(password)
        log.expect("#|$",timeout=60)
        log.sendline('terminal len 0')
        log.expect('#|$')
      else:
        log.sendline('\n')
      print log.before
      return log
    except:
       print "Problem using Telnet to",ipport
       print login.before
       return "ERROR"
  elif terms==0:
      login=pexpect.spawn (syntax2)
      login.expect("[P|p]assword:", timeout=80)
      time.sleep(0.3)
      login.sendline(ts_password)
      login.expect('#|$')
      return login

