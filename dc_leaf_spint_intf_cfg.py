#!/usr/bin/python
from netmiko import ConnectHandler
import re
import inc
import sys
import intf
import os
import time
import net_parse
import multiprocessing
import commands


def read_connect_dev():
        host = open('host_map.cfg','r')
        host_temp = host.read()
        host_data = re.split('\n',host_temp)
        host.close()
        return host_data



spine_ip = '172.29.165.18'
print 'Starting to Configure Spine'
process = multiprocessing.Process(target=intf.SPINE_CFG, args = (spine_ip,))
process.start()
print 'Process Started'
process.join()
print 'Process Ended'

sys.exit()
param=net_parse.DICT('device.cfg')

ip_to_host={}

leaf_devices = read_connect_dev()
for leaf in leaf_devices:
        for dev in param:
                if leaf == dev['host_name']:
                        ip_to_host[dev['mgmt_ip']] = dev['host_name']


jobs=[]
cfgs=[]
for ip,host in ip_to_host.items():
        print ip,host
        process = multiprocessing.Process(target=intf.LEAF_CFG, args = (ip,))
        print "Batched copy for{}: {} ".format(host,ip)
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


