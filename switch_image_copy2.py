#/usr/bin/
import sys
import pexpect
import re
import os
import time
import bootflash_size
import commands

def PARSE(data,value):
	check = re.findall(value,data)
	if check:
		print '{} Matched'

def SPAWN(cli):
	handler = pexpect.spawn(cli)
	time.sleep(0.5)
	handler.expect('assword:|login:|Are you sure you want to continue|assword')
	value = handler.before + handler.after
	print value
	return handler, value

def SEND(handler, cli, expectv = '.*',timeout = 45, skip = 0):
	handler.sendline(cli)
	if skip == 0:
		handler.expect(expectv,timeout)
	elif skip == 1:
		handler.expect('.*', timeout = None)
	time.sleep(0.5)
	value = handler.before + handler.after
	print value 
	return value

def FREESPACE(handler,router_name):
	data = SEND(handler, 'dir bootflash:',router_name)
	free_space = int(re.findall('(\d+) bytes free',data)[0])
	print free_space
	return free_space

def SWITCH_COPY(router_ip,router_name, username = 'admin', server_ip = '172.29.167.113', IMAGENAME = '/root/asadayan-home/nxos.7.0.3.I7.5.bin'):
	# Image name need to be with Image path
	# Host name is the server hostname
	password = 'Cisco12345'
	check = 0
	image = re.split('/',IMAGENAME)[-1]
	copy_syntax = 'copy scp://root@{}{} bootflash: vrf management'.format(server_ip, IMAGENAME)
	ssh_syntax = 'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {}@{}'.format(username,router_ip)
	handler, value = SPAWN(ssh_syntax)
	if re.findall('assword:',value):
		data = SEND(handler,password)
	elif re.findall('RSA key fingerprint',value):
		data = SEND(handler,'yes')
	elif re.findall('login:',value):
		print 'Asking username inspite of giving username: {}'.format(username)
		print 'Aborting the copy for the device {}:{}'.format(router_name, router_ip)
	data = SEND(handler,'term len 0',router_name)
	data = SEND(handler, 'term width 511',router_name)
	free_space = FREESPACE(handler, router_name)
	srv_hn, srv_val = SPAWN('ssh root@172.29.167.113')
	if re.findall('password', srv_val):
  srv_data = SEND(srv_hn,'roZes123','login:')
