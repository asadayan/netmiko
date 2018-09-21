#!/usr/bin/python
from netmiko import ConnectHandler
def CFG(ip,username='admin',password='Cisco12345',sys_vlan=0,no=0):
        device = {
                'device_type':'cisco_nxos',
                'ip':ip,
                'username':username,
                'password':password
                }
        #debug = True
        net_connect = ConnectHandler(**device)
        dev = net_connect.find_prompt()
        vxlan_cli = ['feature vpc','feature bgp', 'feature ospf', 'feature vn-segment-vlan-based', 'feature nv overlay','feature interface-vlan','nv overlay evpn','fabric forwarding anycast-gateway-mac 0000.face.feed']
        vxlan_cli1 = ['feature bgp', 'feature ospf', 'feature vn-segment-vlan-based', 'feature nv overlay','nv overlay evpn','fabric forwarding anycast-gateway-mac 0000.face.feed']

        
        if int(no) == 1:
                vxlan_cli = ['no '+x for x in reversed(vxlan_cli)]
                print "The following cli's are applied on the device {}: {}".format(dev,ip)
                for i in vxlan_cli:
                        print i
        else:
                print "The following cli's are applied on the device {}: {}".format(dev,ip)
                #for i in vxlan_cli:
                        #print i
        en = net_connect.enable() # enter enable mode
        print en
        for command in vxlan_cli:
                cli = net_connect.send_config_set(command,delay_factor=2) # send the commands from our list
                print cli
        cli = net_connect.send_config_set('ntp server 10.81.124.160 use-vrf management',delay_factor = 1)
        print cli
        cli = net_connect.send_config_set('feature bfd',delay_factor = 1)
        print cli
        cli = net_connect.send_config_set('copy running start',delay_factor = 2)
        print cli
                        
        net_connect.disconnect() # close the connection gracefully
                                 
