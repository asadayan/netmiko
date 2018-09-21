#/usr/bin/
import sys
import pexpect
import re
import os
import time
import svi_vrf
import multiprocessing

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
    print "Problem while setting boot string",name,e
    print login.before
    return "ERROR"



if len(sys.argv) !=2:
  print "Usage !! python2 dc_switchport.py switcport.cfg"
  print "see the sample switchport.cfg file for data input"
  sys.exit()

#sys.exit()
passw='Cisco12345'
keys=[]
filename=sys.argv[1]
file=open(filename,'r')
data=file.read()
#print data
info=re.split('\n',data)
keys=re.split(',',info[0])
#print keys
info.pop(0)
#print info
cli={}
fdata=[]
for i in info:
    d=re.split(',',i)
    cli=dict(zip(keys,d))
    fdata.append(cli)

print fdata

for i in fdata:

  if len(i)>=5:
    #print i
    i['process']=multiprocessing.Process(target=svi_vrf.SVI, args=(i,))
    i['process'].start()
  else:
      print "input error"
      sys.exit()

for i in fdata:
  if i['process']:
    i['process'].join()




