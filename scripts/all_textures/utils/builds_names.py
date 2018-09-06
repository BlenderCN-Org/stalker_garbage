import os
buildsList = []
for dir in os.listdir('.'):
    splitDir = dir.split(' ')
    if len(splitDir) > 3:
        if splitDir[0].upper() == 'XRCORE' and splitDir[1].upper() == 'BUILD':
            buildsList.append(splitDir[2])
        elif splitDir[0].upper() == 'XRAY' and splitDir[1].upper() == 'ENGINE' and splitDir[2].upper() == 'BUILD':
            buildsList.append(splitDir[3])
        elif splitDir[0].upper() == 'XRAY' and splitDir[1].upper() == 'ENGINE' and splitDir[2].upper() == 'DEMO':
            buildsList.append(splitDir[4])
buildsList.sort()
for build in buildsList:
    print(build, sep='', end=', ')
input()