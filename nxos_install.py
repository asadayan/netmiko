#!/usr/bin/python
from netmiko import ConnectHandler
import pexpect
import re
import time

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
	data = SEND(handler, 'dir bootflash:','\d{4,25} bytes free')
	free_space = int(re.findall('(\d+) bytes free',data)[0])
	print free_space
	return free_space

def NXOS_INSTALL(router_ip,router_name, IMAGENAME = '/root/asadayan-home/nxos.7.0.3.I7.5.bin', username = 'admin', password='Cisco12345', server_ip = '172.29.167.113'):
                device = {
                        'device_type':'cisco_nxos',
                        'ip':router_ip,
                        'username':username,
                        'password':'Cisco12345',
                        }
                linux = {
                        'device_type':'linux',
                        'ip':server_ip,
                        'username':'root',
                        'password':'roZes123',
                        }
                #debug = True
                image = re.split('/',IMAGENAME)[-1]
                print 'Image Name: {}'.format(image)
                password = 'Cisco12345'
                copy_syntax = 'copy scp://root@{}{} bootflash: vrf management use-kstack'.format(server_ip, IMAGENAME)
                ssh_syntax = 'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {}@{}'.format(username,router_ip)
                net_connect = ConnectHandler(**device)
                dev = net_connect.find_prompt()
                print 'connected to {}'.format(dev)
                net_connect.send_command('term len 0')
                net_connect.send_command('term width 511')
                bootflash_images = net_connect.send_command('dir bootflash:')
                print bootflash_images
                free_space = int(re.findall('(\d+) bytes free',bootflash_images)[0])
                temp = re.findall('(\d+).*{}'.format(image),bootflash_images)
                print temp
                if temp:
                        cimage = int(temp[0])
                else:
                        cimage = 0
                print 'Free space available: {}'.format(free_space)

                #server_connect = ConnectHandler(**linux)
                #files = server_connect.send_command('ls -ltr /root/asadayan-home/{}'.format(image))
                #print files
                #return 0

                srv_hn, srv_val = SPAWN('ssh root@172.29.167.113')
                if re.findall('password', srv_val):
                        srv_data = SEND(srv_hn,'roZes123','login:')
                elif re.findall('fingerprint', srv_val):
                        srv_data = SEND(srv_hn, 'yes','assword')
                        srv_data = SEND(srv_hn,'roZes123','login:')
                else:
                        print 'Login to image_server failed exiting program'
                        return 0
                srv_data = SEND(srv_hn,'ls -ltr {}'.format(IMAGENAME),'\d{6,12}')
                img_size = int(re.findall('\d{6,23}', srv_data)[0])
                print 'free_space: {}, img_size: {}'.format(free_space,img_size)
                if (free_space - img_size) > 500:
                        print 'Space available for Image at bootflash'
                        dev = net_connect.find_prompt()
                        print 'connected to {}'.format(dev)
                        net_connect.send_command('term len 0')
                        net_connect.send_command('term width 511')
                        copy = 'copy scp://root@{}{} bootflash: vrf management'.format(server_ip, IMAGENAME)
                        config = net_connect.send_command_timing(copy)
                        print config
                        if 'password:' in config:
                                config += net_connect.send_command_timing('roZes123',delay_factor = 10)
                                print config
                        elif 'Are you sure you want to continue connecting' in config:
                                config += net_connect.send_command_timing('yes')
                                print config
                                config += net_connect.send_command_timing('roZes123',delay_factor = 10)
                                print config
                        elif cimage and cimage != img_size:
                                config += net_connect.send_command_timing('y')
                                print config
                                config += net_connect.send_command_timing('roZes123', delay_factor = 10)
                        elif cimage and cimage == img_size:
                                print 'Image {} already copied !! Exiting Program for device {}'.format(image,dev)
                                net_connect.disconnect()
                                return 0



                        install ='install all nxos bootflash:{}'.format(image)
                        
                        
                        config = net_connect.send_command(install,expect_string ='Do you want to continue with the installation',delay_factor=10)
                        print config
                        if 'Do you want to continue with the installation' in config:
                                config += net_connect.send_command_timing('y')
                        print config
                        #prompt = net_connect.find_prompt(delay_factor=10)
                        #print prompt
                        net_connect.disconnect()
                
                
                
