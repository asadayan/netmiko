#!/usr/bin/python
from netmiko import ConnectHandler
import re
import inc

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
 
        # Vxlan Config
        spine1_lo0 = '3.101.1.1'
     
        spine2_lo0 = '3.102.1.1'
      
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
   

 
        vrf_set_1 = 20
        vrf_set_2 = 200
        vnid = 100000
        vlanset1 = 101
        vlanset2 = 200
        
        
        mcast_grp1 = '239.1.1.1'
        mcast_grp2 = '239.2.1.1'
        ###############
                             
           

        vxlan_map1 =[]
        vxlan_map2 =[]

        ########
        evpn1 =[]
        evpn2= []
        nve_cli=[]
        for vni in range(vlanset1,vlanset1+20):
                temp3=['evpn','{} vni {} l2'.format(NO,vni),'rd auto','route-target import auto','route-target export auto']
                evpn1.append(temp3)
 
        for vni in range(vlanset2,vlanset2+200):
                temp3=['evpn','{} vni {} l2'.format(NO,vni),'rd auto','route-target import auto','route-target export auto']
                evpn2.append(temp3)                          
         #####
                               
        
  
                
 
       

        ##### Applying Config

 
        output = net_connect.send_config_set(['vrf context T1','rd auto'])
        print output
        output = net_connect.send_config_set(['vrf context T2','rd auto'])
        print output
        output = net_connect.send_config_set(['hardware access-list tcam region vacl 0', 'hardware access-list tcam region arp-ether 256'])
        print output
        for command in evpn1:
                output = net_connect.send_config_set(command,delay_factor=2)
                print '===> {}:\n {}'.format(prompt,output)
                ERR(output,prompt,ip)

        for command in evpn2:
                output = net_connect.send_config_set(command,delay_factor=2)
                print '===> {}:\n {}'.format(prompt,output)
                ERR(output,prompt,ip)

        output = net_connect.send_config_set('copy runn startup')
        print output
                                             
        net_connect.disconnect()


                
                
                
