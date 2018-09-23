#/usr/bin/
import sys
import pexpect
import re
import os
import time
import net_parse
import multiprocessing
import commands


def PING(device):
    pingv = 'ping {} -c 5'.format(device['HostIP'])
    pdata = commands.getoutput(pingv)
    pingd = re.findall('(\d+)% packet loss',pdata)
    ping = int(pingd[0])
    print '{} Ping loss {}% for  {}'.format(device['HostName'],ping,device['HostIP'])
    if ping == 0:
      fn = open('active_leafs.txt','a')
      fn.write('{}\n'.format(device))
      fn.close()
    else:
      fn = open('dead_leafs.txt','a')
      fn.write('{}\n'.format(device))
      fn.close()


if len(sys.argv) !=3:
  print "Usage !! python2 bulk_img_copy.py device_paramater_file ping_check=0 or 1 "
  sys.exit()


device_info=open('map.cfg','r')
device_all = device_info.read()
device_list = re.split('\n',device_all)
device_dict = {}
dict_list=[]

for device in device_list:
        data = re.split('\s',device)
        #print data
        for item in data:
                #print item
                tp = re.split(':',item)
                #print tp[0],tp[1]
                if tp[0] and tp[1]:
                        device_dict[tp[0]] = tp[1]
                #print device_dict
        dict_list.append(device_dict)
        #print dict_list
        device_dict = {}
  

input=sys.argv[1]
ping_check = int(sys.argv[2])
if int(ping_check) == 0:
  print 'Please give param 1 for ping check'
  sys.exit()
param=net_parse.DICT(input)

jobs=[]
cfgs=[]

for i in param:
    device_present = 0
    if  i['host_name'][0:1] == '#' :
        continue
    elif len(i) > 1:
      for device in dict_list:
        if device and device['HostIP'] == i['mgmt_ip']:
          device_present = 1
          process = multiprocessing.Process(target=PING, args = (device,))
          jobs.append(process)
          break
              
    if device_present == 0:
          print 'Term Server info not found for {} : {} '.format(i['host_name'],i['mgmt_ip'])
          fn = open('device_not_found.cfg','a')
          fn.write('Term Server info not found for {} : {} \n'.format(i['host_name'],i['mgmt_ip']))
          fn.close()

#print jobs
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
