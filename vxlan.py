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
        
        if model:
                hw_cli += ['hardware access-list tcam region  span 0','hardware access-list tcam region ifacl  0',
                           'hardware access-list tcam region arp-ether 256 double-wide ']
                print 'Device {} : TOR Model: {} Need TCAM carving'.format(prompt[:-1],model[0])
                reboot = 1
        else:
                reboot = 0
        
        #####
        global_feature = ['feature lldp', 'feature ospf', 'feature pim', 'feature bgp', 'feature lacp', 'feature bfd', 'feature pbr','feature interface-vlan',' no feature tunnel']
        vxlan_cli = ['feature vpc', 'feature vn-segment-vlan-based', 'feature nv overlay','nv overlay evpn','fabric forwarding anycast-gateway-mac 0000.face.feed']
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
   

        print '{} loopback0 ip: {}, loopback1 ip: {}'.format(prompt[:-1],loop0_ip,loop1_ip)
        ###########
        loopback0 = ['{} int loopback 0'.format(GLOB),'ip address {}/32'.format(loop0_ip), 'ip pim sparse-mode', 'ip router ospf 1 area 0.0.0.0','no shut']
        loopback1 = ['{} int loopback 1'.format(GLOB),'ip address {}/32'.format(loop1_ip), 'ip pim sparse-mode', 'ip router ospf 1 area 0.0.0.0','no shut']
        
        ######
        ospf = ['router ospf 1','bfd']

        vrf_set_1 = 20
        vrf_set_2 = 200
        vnid = 100000
        vlanset1 = 101
        vlanset2 = 1101
        
        
        mcast_grp1 = '239.1.1.1'
        mcast_grp2 = '239.2.1.1'
        ###############
                             
        rp = ['{} ip pim rp-address {} group-list 239.0.0.0/8'.format(NO,spine_anycast)]
        bgp =['{} router bgp {}'.format(GLOB,bgp_as), 'neighbor-down fib-accelerate', 'router-id {}'.format(loop0_ip), 'address-family ipv4 unicast',
              '{} neighbor {}'.format(NO,spine1_lo0),'remote-as {}'.format(remote_as),'update-source loopback0', 'address-family l2vpn evpn','send-community extended',
              '{} neighbor {}'.format(NO,spine2_lo0),'remote-as {}'.format(remote_as),'update-source loopback0', 'address-family l2vpn evpn','send-community extended']

        bgp_vrf = ['{} vrf T{}'.format(NO,x) for x in range(1,vrf_no+1)]

        vrf_cfg = []

        #######
        nve_cli_g =  ['{} int nve 1'.format(GLOB), 'no shut', 'host-reachability protocol bgp','source-interface loopback1',
                    'source-interface hold-down-time 400']
        for vrf in range(1,vrf_no+1):
                
                temp = ['{} vrf context T{}'.format(GLOB,vrf),'{} vni {}'.format(NO,vnid+vrf),' address-family ipv4 unicast','route-target both auto',
                               'route-target both auto evpn','address-family ipv6 unicast','route-target both auto','route-target both auto evpn']
                vrf_cfg += temp
                nve_cli_g.append('{} member vni {} associate-vrf'.format(NO,vnid+vrf))
                        
        for vrf in bgp_vrf:
                bgp.append(vrf)
                bgp.append('address-family ipv4 unicast')
                bgp.append('advertise l2vpn evpn')


        

        vxlan_map1 =[]
        vxlan_map2 =[]

        ########
        evpn1 =[]
        evpn2= []
        nve_cli=[]
        for vni in range(vlanset1,vlanset1+20):
                temp1 = ['int nve 1','{} member vni {}'.format(NO,vni),'suppress-arp','mcast-group {}'.format(mcast_grp1),
                        'mcast-group {}'.format(mcast_grp1) ]
                temp2=['{} vlan {}'.format(NO,vni),'vn-segment {}'.format(vni)]
                temp3=['evpn','{} vni {} l2'.format(NO,vni),'rd auto','route-target import auto','route-target export auto']
                nve_cli.append(temp1)
                vxlan_map1.append(temp2)
                evpn1.append(temp3)
                mcast_grp1 = inc.IP_SUBNET(mcast_grp1,net_incr=0,host_incr=1)
        for vni in range(vlanset2,vlanset2+200):
                temp1 = ['int nve 1','{} member vni {}'.format(NO,vni),'suppress-arp','mcast-group {}'.format(mcast_grp2),
                'mcast-group {}'.format(mcast_grp2) ]
                temp2=['{} vlan {}'.format(NO,vni),'vn-segment {}'.format(vni)]
                temp3=['evpn','{} vni {} l2'.format(NO,vni),'rd auto','route-target import auto','route-target export auto']
                nve_cli.append(temp1)
                vxlan_map2.append(temp2)
                evpn2.append(temp3)                          
                mcast_grp2 = inc.IP_SUBNET(mcast_grp2,net_incr=0,host_incr=1)                
 
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
  
        
        for command in vxlan_cli:
                command = command.strip()
                output = net_connect.send_config_set(command,delay_factor=2)
                print '===> {}:\n {}'.format(prompt,output)
                ERR(output,prompt,ip)
                
        output = net_connect.send_config_set(hw_cli,delay_factor=2)
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

        
        output = net_connect.send_config_set(vrf_cfg,delay_factor=2)
        print '===> {}:\n {}'.format(prompt,output)
        ERR(output,prompt,ip)

        
        output = net_connect.send_config_set(bgp,delay_factor=2)
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

        
        output = net_connect.send_config_set(nve_cli_g,delay_factor=2)
        print '===> {}:\n {}'.format(prompt,output)
        ERR(output,prompt,ip)

        for command in nve_cli:
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

        if reboot == 1:
                output = net_connect.send_command('reload')
                print output
                ERR(output,prompt,ip)
                output = net_connect.send_command('yes')
                print output
                ERR(output,prompt,ip)
                

        net_connect.disconnect()


                
                
                
