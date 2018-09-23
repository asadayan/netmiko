#!/usr/bin/python
from netmiko import ConnectHandler
import re
import inc
import sys
import reboot_cfg
import os
import time
import net_parse
import multiprocessing
import commands


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
for device in dict_list:
        print device




jobs=[]
cfgs=[]
for device  in dict_list:
        if device:
                print device
                process = multiprocessing.Process(target=reboot_cfg.RELOAD, args = (device['TermServerIP'],device['TermServerPort'],device['HostIP'],device['HostName'],))
                print "Batched copy for{}: {} ".format(device['HostName'],device['HostIP'])
                jobs.append(process)

       
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


