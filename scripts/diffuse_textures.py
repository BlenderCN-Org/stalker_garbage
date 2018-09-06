import os, time


st = time.time()
passDir = ('act', 'artifact', 'award', 'controller', 'decal', 'ed', 'editor',
'internal', 'detail', 'fx', 'glow', 'grad', 'intro', 'lights', 'map', 'outro',
'pfx', 'sky', 'staff', 'terrain', 'ui', 'water', 'wm', 'wpn', 'andy', 'car',
'effects', 'flare', 'fonts', 'hud', 'human', 'icon', 'jeffry', 'level', 'lod',
'pda', 'sleep', 'temp')
for dir in os.listdir():
    if len(dir.split('.')) == 1 and dir not in passDir:
        for file in os.listdir(dir):
            name, ext = file.split('.')
            if ext == 'dds' and name.split('_')[-1] not in ('bump', 'bump#'):
                oldFile = open(dir + '\\' + file, 'rb')
                data = oldFile.read()
                oldFile.close()
                newDir = 'D:\\save\\' + dir + '\\'
                if not os.access(newDir, os.F_OK):
                    os.makedirs(newDir)
                if os.access(newDir + name + '.dds', os.F_OK):
                    newFile = open(newDir + 'dubli\\' + name + '.dds', 'wb')
                else:
                    newFile = open(newDir + name + '.dds', 'wb')
                newFile.write(data)
                newFile.close()
print(time.time() - st)
input()