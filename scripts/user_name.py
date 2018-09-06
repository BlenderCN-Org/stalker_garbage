import os


compName = os.environ['COMPUTERNAME']
userName = os.environ['USERNAME']
print('\\\\{}\\{}'.format(compName, userName))
input()