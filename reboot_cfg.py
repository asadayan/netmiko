#/usr/bin/
import sys
import telnetlib
import time
import inc
import re



def cli_complete_check(tn,cli,host_name):
  time.sleep(2)
  tn.write(cli)
  data  = tn.read_very_eager()
  info_login = re.findall('login:|#',data)
 
  if info_login:
    print '{} -->Going to Reboot..'.format(host_name)
    print info_login
    return info_login
  
  
def config_ip_only(tn,ipaddress,host_name):
  config = 'reload\n'
  fn = open('rload.cfg','a+')
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
      fn.write('{}  ->{}\n'.format(host_name,data))
      tn.write('y\n')
      time.sleep(3)
      data = tn.read_very_eager()
      print data
      fn.write('{}  ->{}\n'.format(host_name,data))
      time.sleep(20)
      data = tn.read_very_eager()
      print data
      fn.write('{}  ->{}\n'.format(host_name,data))
      data = '{},{}\n'.format(host_name[:-1],ipaddress)
      fn.write('{}  ->{}\n'.format(host_name,data))
      tn.close()
      fn.close()
      return 1



def config_ip(tn,ipaddress,host_name):
  config = 'reload\n'
  fn = open('reload.cfg','a+')
  tn.write('\n')
  time.sleep(3)
  tn.write('\n')
  data = tn.read_until('login:')
  print '{}-->{}'.format(host_name,data)
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
      fn.write('{}  ->{}\n'.format(host_name,data))
      tn.write('y\n')
      time.sleep(3)
      data = tn.read_very_eager()
      print data
      fn.write('{}  ->{}\n'.format(host_name,data))
      time.sleep(20)
      data = tn.read_very_eager()
      data = '{},{}\n'.format(host_name[:-1],ipaddress)
      fn.write('{}  ->{}\n'.format(host_name,data))
      tn.close()
      fn.close()
      return 1

def RELOAD(termservip,port,ipaddress,host_name):
  tn = telnetlib.Telnet()
  tn.open(termservip,port,10)
  check = cli_complete_check(tn,'\n',host_name)
  check = cli_complete_check(tn,'\n',host_name)

  if check and check[0] == 'login:':
    config_i = config_ip(tn,ipaddress,host_name)
  
  elif check[0] == '#':
    config_i = config_ip_only(tn,ipaddress,host_name)
               
  else:
    print 'Error doing telnet'


