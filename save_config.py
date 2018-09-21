#/usr/bin/
import pexpect
import re
import time


def CFG(ip,username,password,prompt):
  syntax="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "+username+"@"+ip
  try:
    login=pexpect.spawn (syntax)
    login.expect("[P|p]assword:", timeout=180)
    login.sendline(password)
    login.expect("#",timeout=60)
    #print login.before
    login.sendline('terminal len 0')
    login.expect('#',timeout=60)
    print "1.======",login.before
    return login
  except Exception as e:
    print "Problem using ssh",e
    print login.before
    return "ERROR"




#sys.exit()
password1='insieme'
password='Cisco12345'
keys=[]
def SAVE(ip,username,password,hostname,reboot='none'):
  login=CFG(ip,'admin',password,'#')
  login.sendline('term width 500')
  login.expect('#',timeout=60)
  login.sendline('term len 0')
  login.expect('#',timeout=60)
  login.sendline('copy running startup')
  login.expect('Copy complete',timeout=60)
  print login.before
  if reboot=='reload':
      login.sendline('reload')
      time.sleep(0.5)
      login.expect('This command will reboot the system.*',timeout=60)
      print login.before
      login.sendline('y')
      login.expect('.*',timeout=60)
      print login.before
      print 'system {}: {} reloaded'.format(hostname,ip)
  login.close()

def SCP(ip,username,password,hostname):
    prompt='{}.*#|Enter|Are you sure you want to continue connecting'.format(hostname)
    login=CFG(ip,'admin',password,prompt)
    login.sendline('term width 500')
    login.expect('#',timeout=60)
    login.sendline('term len 0')
    login.expect('#',timeout=60)
    cmd='copy running-config scp://root@172.29.167.113/root/configs/SalesForce/{}-dhcp-{}.cfg vrf management'.format(hostname,'-'.join(time.ctime().split()))
    login.sendline(cmd)
    resp=0
    resp=login.expect(['ingerprint','assword','Permission denied',':\w\w{0,26}'])
    secret='roZes123'
    print 'Response = {}'.format(resp)

    if resp==1:
       print resp,login.before,login.after
       try:
         login.sendline(secret)
         login.expect('Copy complete\.',timeout=60)
         print "Started Copying from switch {} when response {}".format(hostname,resp)
         print login.before
       except Exception, e:
         print 'Timed out while excepting response for copying for {}'.format(hostname)
         print str(e)

    elif resp==2:
        print 'permission denied'

    else:
       print 'Adding secured hosts'
       try:
         login.sendline('yes')
         login.expect('assword',timeout=60)
         login.sendline(secret)
         login.expect('Copy complete\.',timeout=30)
         print "Started Copying from switch {} when response {}".format(hostname,resp)
       except Exception ,e:
         print 'Timed out while excepting response for copying for {}'.format(hostname)
         print str(e)

    login.close()
    return 0
