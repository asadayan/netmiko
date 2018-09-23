#/usr/bin/
import sys
import telnetlib
import time
import inc
import re



def cli_complete_check(tn,cli,resp=0):
  time.sleep(2)
  tn.write(cli)
  if resp != 0:
    data = 0
  data  = tn.read_very_eager()
  info_login = re.findall('login:|#',data)
  info_poap = re.findall('Abort Auto Provisioning.*',data)
  if info_login:
    print 'Need to configure Host_name, IP and static route'
    print info_login
    return info_login
  elif info_poap:
    print 'Need to diable POAP and setup intial config'
    print info_poap
    return info_poap
  
def config_ip_only(tn,ipaddress,host_name):
  config = 'config t\n'
  mgmt = 'int mgmt0\n'
  ip = "ip address {}/24\n".format(ipaddress)
  mgmt_ip = ip
  vrf = "vrf context management\n"
  route = "ip route 0/0 172.22.132.1\n"
  host = 'hostname {}\n'.format(host_name)
  save = 'copy runn start\n'
  tn.write('\n')
  time.sleep(3)
  tn.write('\n')
  data = tn.read_until('#')
  print data
  if data:
      tn.write(config)
      time.sleep(3)
      data = tn.read_very_eager()
      print data
      tn.write(mgmt)
      time.sleep(3)
      data = tn.read_very_eager()
      print data
      tn.write(mgmt_ip)
      time.sleep(3)
      data = tn.read_very_eager()
      print data
      tn.write(vrf)
      time.sleep(3)
      data = tn.read_very_eager()
      print data
      tn.write(route)
      time.sleep(3)
      data = tn.read_very_eager()
      print data
      tn.write(host)
      time.sleep(3)
      data = tn.read_very_eager()
      print data
      tn.write(save)
      time.sleep(10)
      data = tn.read_very_eager()
      print data
      fn = open('rack7.cfg','a+')
      data = '{},{}\n'.format(host_name[:-1],ipaddress)
      fn.write(data)
      tn.close()
      fn.close()
      return 1



def config_ip(tn,ipaddress,host_name):
  config = 'config t\n'
  mgmt = 'int mgmt0\n'
  ip = "ip address {}/24\n".format(ipaddress)
  mgmt_ip = ip
  vrf = "vrf context management\n"
  route = "ip route 0/0 172.22.132.1\n"
  host = 'hostname {}\n'.format(host_name)
  save = 'copy runn start\n'
  tn.write('\n')
  time.sleep(3)
  tn.write('\n')
  data = tn.read_until('login:')
  print data
  tn.write('admin\n')
  time.sleep(3)
  data = tn.read_until('assword:')
  print data
  passw = re.findall('assword:',data)
  if passw:
    tn.write('Cisco12345\n')
    time.sleep(3)
    data = tn.read_very_eager()
    print data
    cfg = re.findall('#',data)
    if cfg:
      tn.write(config)
      time.sleep(3)
      data = tn.read_very_eager()
      print data
      tn.write(mgmt)
      time.sleep(3)
      data = tn.read_very_eager()
      print data
      tn.write(mgmt_ip)
      time.sleep(3)
      data = tn.read_very_eager()
      print data
      tn.write(vrf)
      time.sleep(3)
      data = tn.read_very_eager()
      print data
      tn.write(route)
      time.sleep(3)
      data = tn.read_very_eager()
      print data
      tn.write(host)
      time.sleep(3)
      data = tn.read_very_eager()
      print data
      tn.write(save)
      time.sleep(10)
      data = tn.read_very_eager()
      print data
      fn = open('rack7.cfg','a+')
      data = '{},{}\n'.format(host_name[:-1],ipaddress)
      fn.write(data)
      tn.close()
      fn.close()
      return 1

def POAP(termservip,port,ipaddress,host_no):
  ip_address = "{}/24\n".format(ipaddress)
  host_name = 'goog-l{}\n'.format(host_no)
  cli1 = "yes\n"
  cli2 = "no\n"
  password = 'Cisco12345\n'
  config = 'config t\n'
  mgmt = 'int mgmt0\n'
  mgmt_ip = ip_address
  vrf = "vrf context management\n"
  route = "ip route 0.0.0.0/24 172.29.165.1\n"
  host = 'host name {}\n'.format(host_name)
  save = 'copy runn start\n'
  po = int(port)
  print termservip,port,ip_address,host_name
  tn = telnetlib.Telnet()
  tn.open(termservip,port,10)
  check = cli_complete_check(tn,'\n')
  check = cli_complete_check(tn,'\n')

  if check and check[0] == 'login:':
    config_i = config_ip(tn,ipaddress,host_name)
  
  elif check[0] == '#':
    config_i = config_ip_only(tn,ipaddress,host_name)


  elif check and check[0] != 'login:':
    tn.write('\n')
    data = tn.read_until('[n]:',5)
    tn.write(cli1)
    time.sleep(0.5)
    data = tn.read_until('[y]:')
    print data
    data =  tn.read_very_eager()
    print data
    tn.write(cli2)
    time.sleep(3)
    data = tn.read_until('Enter the password for')
    print data
    data = tn.read_very_eager()
    print data
    tn.write(password)
    time.sleep(3)
    data = tn.read_until('password')
    print data
    data = tn.read_very_eager()
    print data
    tn.write(password)
    time.sleep(3)
    data = tn.read_until('(yes/no):')
    print data
    data = tn.read_very_eager()
    print data
    tn.write(cli2)
    time.sleep(3)
    data = tn.read_until('login:')
    print data
    data = tn.read_very_eager()
    print data
    config_i = config_ip(tn,ipaddress,host_name)
    
  else:
    print 'Error doing telnet'


ip = '172.22.132.121'
host_no = 275
term_serv = '172.29.165.13'
port = 2089

for items in range(2033,2064):
  port = items
  try:
    data = POAP(term_serv, port, ip, host_no)
  except:
    fa = open('error.cfg','a')
    print '#Error in configuring termserver :{} port: {} for host:goog-l{} ipaddress{}\n'.format(term_serv,port,host_no,ip)
    fa.write('#Error in configuring termserver :{} port: {} for host:goog-l{} ipaddress{}\n'.format(term_serv,port,host_no,ip))
    fa.close()
  ip = inc.IP_SUBNET(ip,net_incr=0,host_incr=1)
  host_no +=1