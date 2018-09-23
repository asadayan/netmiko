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
        hw_cli = []
        data = net_connect.send_config_set('show mod')
        model = re.findall('N9K-C9372PX',data)
        
        
        global_feature = ['no router bgp 65001','no feature bgp' ]
 
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
        
       
        bgp =['{} router bgp {}'.format(GLOB,bgp_as), 'neighbor-down fib-accelerate', 'router-id {}'.format(loop0_ip), 'address-family ipv4 unicast',
              '{} neighbor {}'.format(NO,spine1_lo0),'remote-as {}'.format(remote_as),'update-source loopback0', 'address-family l2vpn evpn','send-community extended',
              '{} neighbor {}'.format(NO,spine2_lo0),'remote-as {}'.format(remote_as),'update-source loopback0', 'address-family l2vpn evpn','send-community extended']

        bgp_vrf = ['{} vrf T{}'.format(NO,x) for x in range(1,vrf_no+1)]


 
                        
        for vrf in bgp_vrf:
                bgp.append(vrf)
                bgp.append('address-family ipv4 unicast')
                bgp.append('advertise l2vpn evpn')


        

        

        ##### Applying Config

        for command in global_feature:
                command = command.strip()
                output = net_connect.send_config_set(command,delay_factor=2)
                print '===> {}:\n {}'.format(prompt,output)
                ERR(output,prompt,ip)


        output = net_connect.send_config_set('feature bgp')
  
 
        output = net_connect.send_config_set(bgp,delay_factor=2)
        print '===> {}:\n {}'.format(prompt,output)
        ERR(output,prompt,ip)

 
 


        
        output = net_connect.send_config_set('copy runn start')
        print output
        ERR(output,prompt,ip)
        print 'Finshed config for device : {}'.format(prompt)

       
                

        net_connect.disconnect()


                
                
                
