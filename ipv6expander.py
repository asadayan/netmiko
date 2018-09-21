#/usr/bin/
import sys
import re
import os

def expand(addr):
    v6addr=['0000','0000','0000','0000','0000','0000','0000','0000']
    v6=re.split(':',addr)
    n=0
    for i in range(0,len(v6)):
        if v6[i] and n<=7:
            v6addr[n]=v6[i].zfill(4)
            n+=1
        elif v6[i]=='':
            n=len(v6addr)-(len(v6)-i)+1

    return v6addr

