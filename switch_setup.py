#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
import sys
import telnetlib
import time

def cli_complete_check(tn):
	data = tn.read_very_eager()
	while  data:
		time.sleep(3)
		data = tn.read_very_eager()
	print 'Cli completed'

def POAP(termservip,port,ipaddress,host_no):
  ip_address = "{}/24\n".format(ipaddress)
  host_name = 'goog-L{}\n'.format(host_no)
  tn = telnetlib.Telnet(termservip,port)
  tn.read_very_eager()
  tn.write("yes\n")
  cli_complete_check(tn)
  tn.write("no\n")
  cli_complete_check(tn)
  tn.write("Cisco12345\n")
  cli_complete_check(tn)
  tn.write("Cisco12345\n")
  cli_complete_check(tn)
  tn.write("no\n")
  cli_complete_check(tn)
  tn.write("config t\n")
  cli_complete_check(tn)
  tn.write("int mgmt0\n")
  cli_complete_check(tn)
  tn.write(ip_address)
  cli_complete_check(tn)
  tn.write("vrf context management\n")
  cli_complete_check(tn)
  tn.write("ip route 0.0.0.0/24 172.29.165.1\n")
  cli_complete_check(tn)
  tn.write(host_name)
  cli_complete_check(tn)
  tn.write("copy runn startup")
  cli_complete_check(tn)
  fn = open('device_info.cfg','a+')
  data = '{},{}\n'.format(host_name[:-1],ipaddress)
  fn.write(data)
  tn.close()

