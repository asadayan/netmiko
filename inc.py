#!/usr/bin/python2
# Author Ahamed Sadayan

import re
import ipv6expander

def PORT(interface='e1/1',step=1,last_port=32,last_sub=4,last_module=16,rnd_robin=0,dev='nexus'):
    '''This method increments the interface given based on a given step. By default the step is one.
    The last port in a module is defined by last_port which is 32 by default. If there is sub modules the last sub module can be dfined by last_sub which is 4 by default and last module is define by last_module which is 16 by default. The increment can be also be round robin by enabling the round_robin flag. This function works by default for nexus switches. This can be altered by defining a flag dev='other'. The following lines gives some examples of incrementing the give
    interfaces.
    inc.PORT(interface='e1/10') --> increments the interface by 1
    inc.PORT(interface='e1/10,step=5) --> increments the interface by 5
    inc.PORT(interface='e1/10,step=5,last_port=24) -- will increment the module after reaching the last port 24. Similarly we can define which is the last sub module and last module which define the base of the sub module and module. '''
    last_port=int(last_port)
    last_sub=int(last_sub)
    last_module=int(last_module)
    rnd_robin=int(rnd_robin)
    data=re.findall('\d+',interface)
    if len(data)==3:
        base=[int(last_module)+1,int(last_sub)+1,int(last_port)+1]
    elif len(data)==2:
        base=[int(last_module)+1,int(last_port)+1]
    inf_name=re.search('[a-zA-Z]+',interface)
    inf_list=[]
    next_value=0
    if inf_name:
       inf_prefix=inf_name.group()
    else:
        print 'Port Parsing Error..'
        return 0
    temp_data=zip(base,data)
    for x,y in enumerate(reversed(temp_data)):
        if len(temp_data)-1==x:
            flag=1
        else:
            flag=0
        if x==0:
            p=int(y[1])+int(step)
        else:
            p=int(y[1])+next_value
        next_value=p/(int(y[0]))
        port=p%int(y[0])
        if dev=='nexus' and port==0: port+=1
        #print 'index :{} Value:{} next_value {} port {}'.format(x,y,next_value,port)
        inf_list.append(str(port))
        if flag==1 and int(rnd_robin)==0 and p>int(y[0])-1:
            print "Port exceeded allocated module"
            return -1
    po='{}{}'.format(inf_prefix,'/'.join(reversed(inf_list)))
    #print inf_list
    return po

def SVI(interface):
    data=re.findall('[a-z]+|\d+',interface)
    data[1]=str(int(data[1])+1)
    inf=''.join(data)
    return inf


def IP_SUBNET(address='1.1.1.1',mask=24,step=1,net_incr=1,host_incr=0,host_step=1,netaddr=0):
    ''' This method takes ipv4 address as the input and increment the subnet with a prefix of /24
    and returns the value by default. The prefix is /24 by default which can be changed by the parameter mask=<no>
    The increment step can be changed by parameter step=<no>. If you the host portion need to be incremented, that can be
    modified with the parameters, host_incr=1(which enables host incrment) and host_step=<nos> , the step for host increment.
    If only the the host part need to be incremented, the subnet/network part can be masked by the paramater net_incr=0
     if netaddr=1 return both network and the ip address
    Ex to increment subnet with a mask of /27: inc.IP_SUBNET(ip_address,mask=27)
    Ex to increment subnet with a mask of /23 and a step of 3: inc.IP_SUBNET(ip_address,mask=23,step=3)
    Ex to increment subnet and host with a subnet mask of 20 and step 2 : inc.IP_SUBNET(ip_address,mask=20,step=2,host_incr=1)
    Ex to increment subnet and host with step: inc.IP_SUBNET(ip_address,step=2,host_incr=1,host_step=2)
    Ex to increment only host: inc.IP_SUBNET(ip_address,net_incr=0,host_incr=1,host_step=2) '''
    mask=int(mask)
    netaddr=int(netaddr)
    if mask==0:
        return address
    value=[]
    net_value=[]
    binary=''
    count=0
    data=re.split('\.',address)
    for i,v in enumerate(data):               # converting the decimal to binary
        data[i]='{0:08d}'.format(int(bin(int(v))[2:]))
        binary=binary+str(data[i])
    bin_list=list(binary)
    net_list=list(binary)
    if net_incr==1:
      while step>0:
        bin_list[mask-1]=int(bin_list[mask-1])+1
        net_list[mask-1]==int(net_list[mask-1])+1
        for index in reversed(range(32)):
            if index >0:
                if bin_list[index]==2:
                    bin_list[index]=0
                    net_list[index]=0
                    bin_list[index-1]=int(bin_list[index-1])+1
                    net_list[index-1]=int(net_list[index-1])+1
        step -=1
    for index in reversed(range(mask,32)):
        net_list[index]=0

    if host_incr==1:
        while host_step >0:
            bin_list[31]=int(bin_list[31])+1
            for index in reversed(range(mask,32)):
                    if index > mask-1:
                      if bin_list[index]==2:
                         bin_list[index]=0
                         bin_list[index-1]=int(bin_list[index-1])+1
            host_step -=1

    binary=''
    net=''
    for i in bin_list:
        binary=binary+str(i)
        count +=1
        if count==8:
            value.append(binary)
            binary=''
            count=0
    count=0
    for i in net_list:
        net=net+str(i)
        count+=1
        if count==8:
            net_value.append(net)
            net=''
            count=0

    for i,v in enumerate(value):
        value[i]=str(int(v,2))
    for i,v in enumerate(net_value):
        net_value[i]=str(int(v,2))

    ip='.'.join(value)
    network='.'.join(net_value)
    if netaddr==1:
        return (network,ip)
    else:
        return ip



def MAC(mac='0000.0000.0001',step=1):
    m=list(mac)
    step=int(step)
    data=[x for x in m if re.search('\d|[a-f]',x)]
    hex_list=[]
    #print 'raw data {}'.format(data)
    for index,v in enumerate(reversed(data)):
        if index==0:
            value=int(v,16)+step
            da=value % 16
            nxt_value = value / 16
            hex_list.append(hex(da)[2:])
            #print 'index {} value{} {} hex_list {}, next value {} , actual_value {}'.format(index,v,value,hex_list,nxt_value,da)
        else:
            value=int(v,16)+nxt_value
            da= value % 16
            nxt_value = value / 16
            hex_list.append(hex(da)[2:])
            #print 'index {} value{} {} hex_list {}, next value {} , actual_value {}'.format(index,v,value,hex_list,nxt_value,da)

    count=1
    output=[]
    for i in reversed(hex_list):
        if count==4:
            output.append(i+'.')
            count=1
        else:
            output.append(i)
            count +=1
    mac_out=''.join(output)
    mac_out=mac_out[:-1]
    return mac_out


def IPv6(address,prefix=64,step=1,host_step=0,host_incr=0,net_incr=1,netaddr=0):
    '''This method takes ipv6 address as the input and increment the subnet with a prefix of /64 and returns the value by default. The prefix is /64 by default which can be changed by the parameter prefix=<no>. The increment step can be changed by parameter step=<no>. If you the host portion need to be incremented, that can bemodified with the parameters, host_incr=1(which enables host incrment) and host_step=<nos> , the step for host increment.
    If only the the host part need to be incremented, the subnet/network part can be masked by the paramater net_incr=0. If netaddr=1 the method returns both network and the ipv6 address
    Ex to increment subnet with a prefix of /64: inc.IPv6(address,prefix=64)
    Ex to increment subnet with a prefix of /72 and a step of 3: inc.IPv6(address,prefix=72,step=3)
    Ex to increment subnet and host with a subnet prefix of 20 and step 2 : inc.IPv6(address,
prefix=72,step=2,host_incr=1)
    Ex to increment subnet and host with step: inc.IPv6(address,step=2,host_incr=1,host_ste
p=2)
    Ex to increment only host: inc.IPv6(address,net_incr=0,host_incr=1,host_step=2) '''

    v6=ipv6expander.expand(address)
    v6addr=[]
    for i in v6:
        temp=list(i)
        v6addr=v6addr+temp
    net_value=[]
    prefix=int(prefix)
    step=int(step)
    host_step=int(host_step)
    host_incr=int(host_incr)
    net_incr=int(net_incr)
    netaddr=int(netaddr)
    binary=''
    bin_list=[]
    if prefix == 0: return address
    for index,value in enumerate(v6addr):
        v6addr[index]='{0:04d}'.format(int(bin(int(value,16))[2:]))
        binary=binary+str(v6addr[index])
    bin_list=list(binary)

    if net_incr :
        while step>0:
            bin_list[prefix-1]=int(bin_list[prefix-1])+1
            for index in reversed(range(128)):
               if index >0:
                   if bin_list[index]==2:
                       bin_list[index]=0
                       bin_list[index-1]=int(bin_list[index-1])+1
            step -=1
    net_list=list(bin_list)
    for index in reversed(range(prefix,128)):
        net_list[index]=-1
    if host_incr:
        while host_step >0:
            bin_list[127]=int(bin_list[127])+1
            for index in reversed(range(prefix,128)):
                    if index > prefix-1:
                      if bin_list[index]==2:
                         bin_list[index]=0
                         bin_list[index-1]=int(bin_list[index-1])+1
            host_step -=1
    binary=''
    net=''
    value=[]
    count=0
    for i in bin_list:
        binary=binary+str(i)
        count +=1
        if count==4:
            value.append(binary)
            binary=''
            count=0
    count=0
    for i in net_list:
        if i != -1:
            net=net+str(i)
            count+=1
            if count==4:
               net_value.append(net)
               net=''
               count=0
    index=0
    ipv6=''
    ipv6_net=''
    for i,v in enumerate(value):
        temp=str(hex(int(v,2))[2:])
        if index < 4:
            ipv6=ipv6+temp
            index +=1
        else:
            ipv6=ipv6+':'+temp
            index=1
    index=0
    for i,v in enumerate(net_value):
        temp=str(hex(int(v,2))[2:])
        if index < 4:
            ipv6_net=ipv6_net+temp
            index +=1
        else:
            ipv6_net=ipv6_net+':'+temp
            index=1
    ipv6_net='{}::/{}'.format(ipv6_net,prefix)
    if netaddr==1:
        return (ipv6_net,ipv6)
    else:
        return ipv6







