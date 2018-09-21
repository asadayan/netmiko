#!/usr/bin/python
from netmiko import ConnectHandler
import re
import inc
def CFG(ip,username='admin',password='Cisco12345',vrf_no=2,no=0,glob_del = 0):
        device = {
                'device_type':'cisco_nxos',
                'ip':ip,
                'username':username,
                'password':password
                }


        net_connect = ConnectHandler(**device)
        prompt = net_connect.find_prompt()
        host_no = re.findall('\d+', prompt)[0]
        host_name=prompt[:-1]
        hw_cli = []
        data = net_connect.send_config_set('show mod')
        model = re.findall('\s+([A-Za-z0-9-]+)\s+active',data)[0]
        env = net_connect.send_command('term len 0')
        print env
        env = net_connect.send_command('term width 511')
        version = net_connect.send_command('show version')
        ver = re.findall('nxos.*bin',version)[0]
        if ver == 'nxos.7.0.3.I7.5.bin':
                print 'System running right version in device {}:{}'.format(host_name,ip)
        else:
                fn = open('dev_miss.cfg','a')
                fn.write('{}     {}    {}   {}\n'.format(host_name,ip,ver,model))
                fn.close
                                 
                
        
       
        net_connect.disconnect()


                
                
                
