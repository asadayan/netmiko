#!/usr/bin/python
from netmiko import ConnectHandler
import re
import inc
def CFG(ip,username='admin',password='Cisco12345',model_check='N9K-C9348GC-FXP'):
        device = {
                'device_type':'cisco_nxos',
                'ip':ip,
                'username':username,
                'password':password
                }

        model_list = ['N9K-C93180YC-EX','N9K-C9348GC-FXP']
        net_connect = ConnectHandler(**device)
        prompt = net_connect.find_prompt()
        host_no = re.findall('\d+', prompt)[0]
        host_name=prompt[:-1]
        hw_cli = []
  
        env = net_connect.send_command('term len 0')
        print env
        env = net_connect.send_command('term width 511')
        #version = net_connect.send_command('show version')
        #ver = re.findall('nxos.*bin',version)[0]

        data = net_connect.send_config_set('show mod')
        model = re.findall('\s+([A-Za-z0-9-]+)\s+active',data)[0]
        if  model == model_check:
                fn = open('device-type.cfg','a')
                print 'Seoul model found in device {}: {}'.format(host_name,ip)
                fn.write('{}     {}     {}\n'.format(host_name,ip,model))
                fn.close()
                
       
        net_connect.disconnect()


                
                
                
