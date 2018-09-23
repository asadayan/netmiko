#/usr/bin/
import sys
import pexpect
import re
import os
import time
import net_parse
import multiprocessing
import commands
import vxlan_evpn_bgp


if len(sys.argv) !=3:
  print "Usage !! python2 bulk_img_copy.py device_paramater_file ping_check=0 or 1 "
  sys.exit()

input=sys.argv[1]
ping_check = int(sys.argv[2])
print input
param=net_parse.DICT(input)
#print param
jobs=[]
cfgs=[]
for i in param:
    if  i['host_name'][0:1] == '#' :
        continue
    elif len(i) > 1:
        ip=i['mgmt_ip']
        if ping_check == 1:
            ping = 0
            pingv = 'ping {} -c 5'.format(ip)
            time.sleep(2)
            pdata = commands.getoutput(pingv)
            pingd = re.findall('(\d+)% packet loss',pdata)
            ping = int(pingd[0])
            print 'Ping loss {}'.format(ping)

        elif ping_check == 0:
            ping = 0
        if ping == 0:
            process = multiprocessing.Process(target=vxlan_evpn_bgp.CFG, args = (ip,))
            print "Batched copy for{}: {} ".format(i['host_name'],ip)
            jobs.append(process)
            print i
        else:
            print 'Switch {}: {} not reachable '.format(ip,i['host_name'])



print jobs
max_thread_cnt = 9
act_thread_cnt = 0
job_wait_q = []
for each_job in jobs:
    each_job.start()
    print '{}'.format('++'*50)
    job_wait_q.append(each_job)
    act_thread_cnt += 1
    print  'Started Job {}'.format(act_thread_cnt)
    if (act_thread_cnt == max_thread_cnt) or (each_job == jobs[-1]):
        print 'Dispatched {} task(s)'.format(act_thread_cnt)
        for jobitem in job_wait_q:
            jobitem.join()
        job_wait_q = []
        act_thread_cnt = 0
