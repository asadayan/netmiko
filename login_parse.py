#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
import re
import pexpect

def PARSE(handler,syntax,EXPECT='.*'):
	print 'Parse module called'
	handler.sendline(syntax)
	handler.expect(EXPECT)
	data1 = handler.before
	data2 = handler.after
	data = data1 + data2
	true = re.findall(EXPECT,data)
    	if true:
    		return true
    	else:
    		return None






