#!/usr/bin/python
import re
import os
import sys

f = open('rack1.cfg','r')
data = f.read()
out = re.split('\n',data)

out.pop(0)
for i in out:
        print i
o = []
fo = open('host.cfg','a')
for i in out:
        o = re.split(',',i)
        if len(o) == 2:
                fo.write('{}     {}\n'.format(o[1],o[0]))

fo.close()
f.close()
        
