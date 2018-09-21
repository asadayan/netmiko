#!/bin/python
import re
import sys
import net_parse
import ssh
import telnet
import pexpect

if len(sys.argv) != 3:
   print "usage python2 console.py <device name> <method cons|ssh>"
   sys.exit()

dev=sys.argv[1]
method=sys.argv[2]
username='admin'
password='Cisco12345'
fdata=net_parse.DICT('device_info.cfg')
for i in fdata:
    if  dev==i['host_name']:
       ip=i['mgmt_ip']
       hostname=i['host_name']

if method=='ssh':
   handler=ssh.SSH(ip,username,password,hostname)
   print "connected to device {}:{}".format(hostname,ip)
   handler.interact()
elif method=='cons':
   terms=0
   handler=telnet.TELNET(ip,username,password,terms)
   handler.interact()

print "connection closed for ip",ip,hostname


