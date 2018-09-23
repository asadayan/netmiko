#!/usr/bin/python
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
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
        device_info=open('map.cfg','r')
        device_all = device_info.read()
        device_list = re.split('\n',device_all)
        device_dict = {}
        dict_list=[]

        for dev in device_list:
                data = re.split('\s',dev)
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
        if no == 1:
                NO = 'no'
        elif no ==0:
                NO =''
        if glob_del == 1:
                GLOB = 'no'
        else:
                GLOB =''
        try:
                net_connect = ConnectHandler(**device)
                prompt = net_connect.find_prompt()
        except:
                for dev in dict_list:
                        if dev and dev['HostIP'] == ip:
                                print 'Cannot SSH to device {} {}'.format(dev['HostName'],ip)
                                fn = open('disabled_device.log','a')
                                fn.write('{}\n'.format(dev))                                       
                sys.exit()
                
        prompt = net_connect.find_prompt()
        host_no = re.findall('\d+', prompt)[0]
 
        
        #####
        global_feature = ['feature interface-vlan', 'evpn']
  

        vrf_set_1 = 20
        vrf_set_2 = 200
        vnid = 100000
        vlanset1 = 101
        vlanset2 = 1101
        
 
        

        vxlan_map1 =[]
        vxlan_map2 =[]

        ########
        evpn1 =[]
        evpn2= []
        nve_cli=[]
        for vni in range(vlanset1,vlanset1+20):
                temp2=['{} vlan {}'.format(NO,vni),'vn-segment {}'.format(vni)]
                temp3=['evpn','{} vni {} l2'.format(NO,vni),'rd auto','route-target import auto','route-target export auto']
                vxlan_map1.append(temp2)
                evpn1.append(temp3)
        for vni in range(vlanset2,vlanset2+200):
                temp2=['{} vlan {}'.format(NO,vni),'vn-segment {}'.format(vni)]
                temp3=['evpn','{} vni {} l2'.format(NO,vni),'rd auto','route-target import auto','route-target export auto']
 
                vxlan_map2.append(temp2)
                evpn2.append(temp3)                          
              
 
        #####
        vlan_cfg1 = ['vlan 101-120','vlan 1001']
        vlan_cfg2 = ['vlan 1101-1300','vlan 2001']

        vlan_int_config = []
        
                                  
        for vlan in range(101,121):
                temp= ['{} int vlan {}'.format(NO,vlan),'no shutdown','vrf member T1','ip address 7.{}.1.1/24'.format(vlan),'ipv6 address 2001:7:{}::1/64'.format(vlan),
                       'fabric forwarding mode anycast-gateway','no ip redirects','no ipv6 redirects','mtu 9216']
                vlan_int_config.append(temp)
  
                
        
        vlan_temp = 1
        for vlan in range(1101,1301):
                temp= ['{} int vlan {}'.format(NO,vlan),'no shutdown','vrf member T2','ip address 9.{}.1.1/24'.format(vlan_temp),'ipv6 address 2001:9:{}::1/64'.format(vlan),
                       'fabric forwarding mode anycast-gateway','no ip redirects','no ipv6 redirects','mtu 9216']
                vlan_int_config.append(temp)
                vlan_temp +=1
        temp = ['{} int vlan 1001'.format(NO),'no shutdown','vrf member T1','mtu 9216','{} int vlan 2001'.format(NO),'no shutdown','vrf member T2','mtu 9216']
    
        vlan_int_config.append(temp)
       

        ##### Applying Config

        for command in global_feature:
                command = command.strip()
                output = net_connect.send_config_set(command,delay_factor=2)
                print '===> {}:\n {}'.format(prompt,output)
                ERR(output,prompt,ip)
  
        
 

        
        output = net_connect.send_config_set(vlan_cfg1,delay_factor=2)
        print '===> {}:\n {}'.format(prompt,output)
        ERR(output,prompt,ip)

        
        output = net_connect.send_config_set(vlan_cfg2,delay_factor=2)
        print '===> {}:\n {}'.format(prompt,output)
        ERR(output,prompt,ip)


        for command in vxlan_map1:
                output = net_connect.send_config_set(command,delay_factor=2)
                print '===> {}:\n {}'.format(prompt,output)
                ERR(output,prompt,ip)

        for command in vxlan_map2:
                output = net_connect.send_config_set(command,delay_factor=2)
                print '===> {}:\n {}'.format(prompt,output)
                ERR(output,prompt,ip)

 
        for command in evpn1:
                output = net_connect.send_config_set(command,delay_factor=2)
                print '===> {}:\n {}'.format(prompt,output)
                ERR(output,prompt,ip)

        for command in evpn2:
                output = net_connect.send_config_set(command,delay_factor=2)
                print '===> {}:\n {}'.format(prompt,output)
                ERR(output,prompt,ip)

        
 
        for command in vlan_int_config:
                output = net_connect.send_config_set(command,delay_factor=2)
                print '===> {}:\n {}'.format(prompt,output)
                ERR(output,prompt,ip)
        output = net_connect.send_config_set('copy runn start')
        print output
        ERR(output,prompt,ip)
        print 'Finshed config for device : {}'.format(prompt)

 
        net_connect.disconnect()


                
                
                
