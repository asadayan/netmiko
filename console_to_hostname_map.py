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
  print 'Getting: {}'.format(info_login)
  return info_login
  



def MAP(termservip,port,ipaddress,host_no):
  tn = telnetlib.Telnet()
  tn.open(termservip,port,10)
  check = cli_complete_check(tn,'\n')
  check = cli_complete_check(tn,'\n')
  fn = open('map.cfg','a')
  if check and check[0] == 'login:':
    tn.write('admin\n')
    data = tn.read_until('assword:')
    tn.write('Cisco12345\n')
    data =  tn.read_until('#')
    time.sleep(2)
    tn.write('show run int mgmt0\n')
    data = tn.read_until('#')
    hostname = re.findall('goog-l\d+',data)
    host_ip = re.findall('\d+\.\d+\.\d+\.\d+',data)
    print data,hostname,host_ip
    fn.write('TermServerIP:{} TermServerPort:{} HostName:{} HostIP:{}\n'.format(termservip,port,hostname[0],host_ip[0]))
  elif check[0] == '#':
    tn.write('\n')
    tn.read_until('#')
    tn.write('show run int mgmt0\n')
    time.sleep(2)
    data = tn.read_very_eager()
    
    hostname = re.findall('goog-l\d+',data)
    host_ip = re.findall('\d+\.\d+\.\d+\.\d+',data)
    print data, hostname,host_ip
    fn.write('TermServerIP:{} TermServerPort:{} HostName:{} HostIP:{}\n'.format(termservip,port,hostname[0],host_ip[0]))
  else:
    print 'Error doing telnet'


ip = '172.29.165.249'
host_no = 2
term_serv_list = ['172.29.165.7','172.29.165.8','172.29.165.9','172.29.165.10','172.29.165.11','172.29.165.12','172.29.165.13','172.29.165.14','172.29.164.15']
term_serv = '172.29.165.14'
port = 2

for items in range(2066,2098):
  port = items
  data = MAP(term_serv, port, ip, host_no)

  