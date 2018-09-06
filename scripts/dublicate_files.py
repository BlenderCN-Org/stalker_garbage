import os

t = open('$.dds', 'rb')
data = t.read()
t.close()

names = []
for f in os.listdir():
    (name, ext) = f.split('.')
    if ext == 'dds' and name != '$':
        newFile = open('copy.dir\\' + name + '.' + ext, 'wb')
        newFile.write(data)
        newFile.close()
input()