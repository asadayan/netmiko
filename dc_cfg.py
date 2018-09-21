#/usr/bin/
import sys
import pexpect
import re
import os
import time
import auto_config
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
  print "Usage !! python2 dc_cfg.py msdc.cfg"
  print "see the sample msdc.cfg file for data input"
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
jobs=[]
for i in fdata:

  if len(i)>=5:
    print i
    i['process']=multiprocessing.Process(target=auto_config.IPCFG, args=(i['mgmt_ip'],'admin',passw,i['host_name'],i['loopback_ip'],i['first_ip'],i['local_as'],i['remote_as'],i['peer_host'],i['mask'],i['bfd'],i['pim'],i['no']))
    jobs.append(i['process'])
  else:
      print "input error"
      #sys.exit()

max_thread_cnt = 5
act_thread_cnt = 0
job_wait_q = []
for each_job in jobs:
    #print (each_job)
    each_job.start()
    job_wait_q.append(each_job)
    act_thread_cnt += 1
    if (act_thread_cnt == max_thread_cnt) or (each_job == jobs[-1]):
        print 'Dispatched {} task(s)'.format(act_thread_cnt)
        for jobitem in job_wait_q:
            jobitem.join()
        job_wait_q = []
        act_thread_cnt = 0




