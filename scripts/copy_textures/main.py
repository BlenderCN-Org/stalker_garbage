import os
f = open('texture_list.txt', 'r')
s = f.read()
f.close()
textures = s.split('\n')
list_dir = {}
path, out, ext = 'E:\\STALKER Game\\CS\\resources\\resources\\textures\\', 'T:\\!TEXTURE_RIP\\', '.dds'
for file_name in textures:
    dir = out + file_name.split('\\')[0]
    if file_name[0] != '$':
        if not list_dir.get(dir):
            list_dir[dir] = True
list_dir = list(list_dir.keys())
list_dir.sort()
if not os.access(out, os.F_OK):
    os.makedirs(out)
for dir in list_dir:
    if not os.access(dir, os.F_OK):
        os.mkdir(dir)
for name in textures:
    sourse = open(path + name + ext, 'rb')
    data = sourse.read()
    sourse.close()
    copy = open(out + name + ext, 'wb')
    copy.write(data)
    copy.close()
input()