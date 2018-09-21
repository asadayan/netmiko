'Learn to communicate with other programs'

from subprocess import Popen, PIPE, check_output
import os


def run_command(cmd):
        if not os.system(cmd + '> temp.txt'):
                raise RuntimeError('Command failed')
        with open('temp.txt') as f:
                s = f.read()
        os.remove('temp.txt') # os.unlink('temp.txt')
        return s


#print run_command('netstat -s').upper()
#print run_command('ping -c 3 www.cisco.com').upper()

#print check_output('netstat -s', shell=True).upper()

if False and __name__ == '__main__':
        print check_output(['netstat', '-s']).upper()
        print check_output(['echo', os.environ['USER']])

        print check_output(['echo', os.path.expanduser('~')])

        s = check_output(['ping', '-c' , '3', 'www.cisco.com'])
        print s
        ping_result = s.splitlines()[-2]
        #assert '0.0%' in ping_result # Create false Positives

        assert '0.0%' in ping_result.split()

p = Popen(['sort'], stdin = PIPE, stdout = PIPE, stderr = PIPE)
text, err = p.communicate(input=__doc__)
print text


p = Popen(['grep','echo'], stdin = PIPE, stdout = PIPE, stderr = PIPE)
text, err = p.communicate(input=__doc__)
print text.upper()




