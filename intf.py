#!/usr/bin/python
from netmiko import ConnectHandler
import re
import inc
import sys

def ERR(data,prompt,ip):
        error = re.findall('% Invalid|\^',data)
        if error:
                filename = '{}-config.log'.format(prompt[:-1])
                fn = open(filename,'w')
                fn.write(data)
                fn.close()
                return 1


def SPINE_CFG(ip,username='admin',password='Cisco12345',no=0,glob_del = 0):
        print 'Inside Interface Module'
        device = {
                'device_type':'cisco_nxos',
                'ip':ip,
                'username':username,
                'password':password
                }

        if no == 1:
                NO = 'no'
        elif no ==0:
                NO =''
        if glob_del == 1:
                GLOB = 'no'
        else:
                GLOB =''
        net_connect = ConnectHandler(**device)
        prompt = net_connect.find_prompt()
        print prompt
        host_no = re.findall('\d+', prompt)[0]
        env = net_connect.send_command('term len 0')
        env = net_connect.send_command('term width 511')
        lldp_data = net_connect.send_command('show lldp nei')
        print lldp_data
        lldp = re.findall('(goog-l\d+)\s+(Eth\d+/\d+)\s+\d+\s+BR\s+(Ethernet\d/\d+)',lldp_data)
        dc_set = 4
        interface_config = []
        fname = open('{}.log'.format(prompt[:-1]),'a')
        host = open('host_map.cfg','a')
        for nei in lldp:
                print nei[0]
                ip_octet = int(re.findall('\d+',nei[0])[0])
                if ip_octet > 254:
                        dc_set = dc_set + ip_octet/255
                        ip_octet = ip_octet % 255
                ip_address = '{}.{}.{}.2'.format(dc_set,ip_octet,host_no)
                print ip_address
                intf_pconfig = net_connect.send_command('show run int {}'.format(nei[1].lower()))
                intf_exist = re.findall('description con to Leaf {} - rem intf {}'.format(nei[0].lower(),nei[2].lower()),intf_pconfig)
                if intf_exist:
                        temp_config = ['int {}'.format(nei[1].lower()), '{} ip address {}/24'.format(NO,ip_address), 'no shutdown', 'mtu 9216',
                                       'no ip redirects','no ipv6 redirects','ip router ospf 1 area 0.0.0.0', 'ip pim sparse-mode',
                                       'ip ospf network point-to-point',
                                       '{} description con to Leaf {} - rem intf {}'.format(NO,nei[0].lower(),nei[2].lower())]
                        interface_config.append(temp_config)
                        host.write('{}\n'.format(nei[0]))
                        print temp_config
        host.close()

                

        ##### Applying Config
 
        for command in interface_config:
                output = net_connect.send_config_set(command)
                fname.write('{} ---> {}\n'.format(prompt[:-1],output))
                ERR(output,prompt[:-1],ip)
                print output
                     
                     
                
        d = net_connect.send_command('copy runn start')
        #fname.write('{} ---> {}\n'.format(prompt[:-1],d))
        net_connect.disconnect()
        fname.close()

def LEAF_CFG(ip,username='admin',password='Cisco12345',no=0,glob_del = 0):
        print 'Inside Interface Module'
        device = {
                'device_type':'cisco_nxos',
                'ip':ip,
                'username':username,
                'password':password
                }

        if no == 1:
                NO = 'no'
        elif no ==0:
                NO =''
        if glob_del == 1:
                GLOB = 'no'
        else:
                GLOB =''
        net_connect = ConnectHandler(**device)
        prompt = net_connect.find_prompt()
        print prompt
        host_no = re.findall('\d+', prompt)[0]
        env = net_connect.send_command('term len 0')
        env = net_connect.send_command('term width 511')
        lldp_data = net_connect.send_command('show lldp nei')
        #print lldp_data
        lldp = re.findall('(goog-s\d+)\s+(Eth\d+/\d+)\s+\d+\s+BR\s+(Ethernet\d/\d+)',lldp_data)
        print lldp
        dc_set = 4
        interface_config = []
        fname = open('{}.log'.format(prompt[:-1]),'a')
        for nei in lldp:
                #print nei[0]
                ip_octet = int(host_no)
                spine_no = int(re.findall('\d+',nei[0])[0])
                if ip_octet > 254:
                        dc_set = dc_set + ip_octet/255
                        ip_octet = ip_octet % 255
                ip_address = '{}.{}.{}.1'.format(dc_set,ip_octet,spine_no)
                print ip_address
                temp_config = ['int {}'.format(nei[1].lower()), 'no switchport','{} ip address {}/24'.format(NO,ip_address), 'no shutdown', 'mtu 9216',
                               'no ip redirects','no ipv6 redirects','ip router ospf 1 area 0.0.0.0', 'ip pim sparse-mode',
                               'ip ospf network point-to-point',
                               '{} description con to Leaf {} - rem intf {}'.format(NO,nei[0].lower(),nei[2].lower())]
                interface_config.append(temp_config)

        for command in interface_config:
                output = net_connect.send_config_set(command)
                fname.write('{} ---> {}\n'.format(prompt[:-1],output))
                ERR(output,prompt[:-1],ip)
                print output
                     
                     
                
        d = net_connect.send_command('copy runn start')
        #fname.write('{} ---> {}\n'.format(prompt[:-1],d))
        net_connect.disconnect()
        fname.close()
        


        
                            



                
                
                
