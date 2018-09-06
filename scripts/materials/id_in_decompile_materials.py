import os

print('SoC Materials id (gamemtl.xr):\n')
ids = []
materials = []
for name in os.listdir():
    nameExt = name.split('.')
    if len(nameExt) > 1:
        ext = nameExt[-1]
        if ext == 'ltx':
            file = open(name, 'r')
            for line in file.readlines():
                if line[:5] == 'id = ':
                    id = int(line[5:-1])
                    ids.append((id, nameExt[0]))
    else:
        for i in os.listdir(name):
            nameExt = i.split('.')
            if len(nameExt) > 1:
                ext = nameExt[-1]
                if ext == 'ltx':
                    file = open(name + '\\' + i, 'r')
                    for line in file.readlines():
                        if line[:5] == 'id = ':
                            id = int(line[5:-1])
                            ids.append((id, name + '\\\\' + nameExt[0]))
ids.sort()
for id, name in ids:
    print('{: <3} :  \'{}\','.format(id, name))
input()