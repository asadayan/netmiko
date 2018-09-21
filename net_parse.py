#!/usr/bin/python2
import re
import sys

# This function read a file with keys being the top line of the file and multiple values on each line and
# returns a list of dictionaries with key value pair.

def DICT(filename):
    keys=[]
    file=open(filename,'r')
    data=file.read()
    #print data
    info=re.split('\n',data)
    keys=re.split(',',info[0])
    #print keys
    info.pop(0)
    #print info
    cli={}
    fdata=[]
    for i in info:
        if len(i) > 0:
            d=re.split(',',i)
            cli=dict(zip(keys,d))
            fdata.append(cli)
    return fdata

