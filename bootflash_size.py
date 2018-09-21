#!/usr/bin/python
import time
import re
import ssh


def BOOTFLASH(ip ,username = 'admin', password = 'Cisco12345', hostname = '#'):
    try:
        hn = ssh.SSH(ip,username,password,hostname)
        hn.sendline('term len 0')
        hn.expect('#',60)
        hn.sendline('term width 511')
        hn.expect('#',60)
        hn.sendline('config t')
        hn.expect('#',60)
        hn.sendline('feature bash')
        hn.expect('#',60)
        hn.sendline('run bash')
        hn.expect('\$',60)
        print hn.before
        hn.sendline('ls -ltr /bootflash/')
        hn.expect('\$',60)
        dat = hn.before
        out = re.split('\n',dat)
        data = []
        #print out
        for i in out:
                tmp = re.split('\s+',i)
                if len(tmp) == 10 and tmp[-2][:4] == 'nxos':
                        data.append(tmp)
        if len(data) > 0:
           del_image = data[0][-2]
        else:
            del_image = 'NULL'
        #print '>>>old image in the system {}<<<'.format(del_image)
        hn.sendline('exit')
        hn.expect('#',60)
        hn.sendline('term len 0')
        hn.expect('#',60)
        hn.sendline('dir bootflash:')
        hn.expect('total',60)
        bspace = re.findall('\d+',hn.before)
        #print bspace
        free_space = int(bspace[-2])
        #print 'Free space in bootflash: {}'.format(free_space)
        hn.close()
        return free_space,del_image
    except:
        print "Bootflash_size: Problem using ssh to",ip
        print hn.before
        return 0,0

