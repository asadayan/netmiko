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


def CFG(ip,username='admin',password='Cisco12345',vrf_no=2,no=0,glob_del = 0):
        device = {
                'device_type':'cisco_nxos',
                'ip':ip,
                'username':username,
                'password':password
                }
        df = open('map.cfg')
        hdata = df.read()
        pdata = re.split('\n',hdata)
        host_name = []
        host_ip = []
        host_data={}
        for items in pdata:
                if 'HostIP' in items:
                        #print items
                        host_name.append(re.findall('HostName:(goog-l\d+)',items)[0])
                        host_ip.append(re.findall('HostIP:(\d+\.\d+\.\d+\.\d+)',items)[0])
        host_data = zip(host_name,host_ip)

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
        host_no = re.findall('\d+', prompt)[0]
        hw_cli = []
 
        lldp_data = net_connect.send_command('show lldp nei')
        lldp = re.findall('(Eth\d+/\d+)\s+\d+\s+BR\s+(Ethernet\d/\d+)',lldp_data)
        
        #####
        global_feature = ['nv overlay evpn','feature lldp', 'feature ospf', 'feature pim', 'feature bgp',  'feature bfd', 'feature pbr',
                          'feature interface-vlan',' no feature tunnel']
     
        # Vxlan Config
        spine_lo0 = '3.{}.1.1'.format(host_no)
        spine_anycast='3.101.102.1'

        bgp_as = '65001'
        remote_as = '65001'
        if int(host_no) < 255:
                loop0_ip = '1.0.{}.1'.format(host_no)
                loop1_ip = '2.0.{}.2'.format(host_no)
        elif int(host_no) > 254:
                h = int(host_no)
                hmod = str(h%255)
                loop0_ip = '1.255.{}.1'.format(hmod)
                loop1_ip = '2.255.{}.2'.format(hmod)
   


        ###########
        loopback0 = ['{} int loopback 0'.format(GLOB),'ip address {}/32'.format(spine_lo0), 'ip pim sparse-mode', 'ip router ospf 1 area 0.0.0.0','no shut']
        loopback1 = ['{} int loopback 1'.format(GLOB),'ip address {}/32'.format(spine_anycast), 'ip pim sparse-mode', 'ip router ospf 1 area 0.0.0.0','no shut']
        
        ######
        ospf = ['router ospf 1','bfd']


        
        mcast_grp1 = '239.1.1.1'
        mcast_grp2 = '239.2.1.1'
        ###############
                             
        rp = ['{} ip pim rp-address {} group-list 239.0.0.0/8'.format(NO,spine_anycast),
              'ip pim anycast-rp 3.101.102.1 3.101.1.1', 'ip pim anycast-rp 3.101.102.1 3.102.1.1' ]

        bgp =['{} router bgp {}'.format(GLOB,bgp_as), 'neighbor-down fib-accelerate', 'router-id {}'.format(spine_lo0), 'address-family ipv4 unicast',
              'address-family l2vpn evpn','retain route-target all', 'template peer VTEP-PEERS', 'remote-as {}'.format(remote_as),
              'update-source loopback0', 'address-family ipv4 unicast', 'send-community both','route-reflector-client',
              'address-family l2vpn evpn', 'send-community both', 'route-reflector-client']

        bgp_client = []

        for device in range(1,255):
                client = ['{} router bgp {}'.format(NO,bgp_as),'neighbor 1.0.{}.1'.format(device), 'inherit peer VTEP-PEERS']
                bgp_client.append(client)
 
        ##### Applying Config

        for command in global_feature:
                command = command.strip()
                output = net_connect.send_config_set(command,delay_factor=2)
                print '===> {}:\n {}'.format(prompt,output)
                ERR(output,prompt,ip)
  
        
        
        output = net_connect.send_config_set(loopback0,delay_factor=2)
        print '===> {}:\n {}'.format(prompt,output)
        ERR(output,prompt,ip)

        
        output = net_connect.send_config_set(loopback1,delay_factor=2)
        print '===> {}:\n {}'.format(prompt,output)
        ERR(output,prompt,ip)

        
        output = net_connect.send_config_set(ospf,delay_factor=2)
        print '===> {}:\n {}'.format(prompt,output)
        ERR(output,prompt,ip)
                
        
        output = net_connect.send_config_set(rp,delay_factor=2)
        print '===> {}:\n {}'.format(prompt,output)
        ERR(output,prompt,ip)

        output = net_connect.send_config_set(bgp,delay_factor=2)
        print '===> {}:\n {}'.format(prompt,output)
        ERR(output,prompt,ip)

        for command in bgp_client:
                output = net_connect.send_config_set(command,delay_factor=2)
                print '===> {}:\n {}'.format(prompt,output)
                ERR(output,prompt,ip)

        net_connect.send_command('copy runn start')
        net_connect.disconnect()


CFG('172.29.165.17')


                
                
                
