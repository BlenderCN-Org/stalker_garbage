import os


for name in os.listdir('new'):
    file = open('new\\{}'.format(name), 'rb')
    new = file.read()
    file.close()
    file = open('old\\{}'.format(name), 'rb')
    old = file.read()
    file.close()
    if old != new:
        print(name)
input()

