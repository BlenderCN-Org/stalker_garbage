import os, struct, time
startTime = time.time()
log = open('dimentions_list.txt', 'w')
print('Level Dimentions by level.cform', file=log)
for level in os.listdir():
    if len(level.split('.')) == 1:   # and level[:7] != 'testers':
        try:
            cform = open(level + '\\level.cform', 'rb')
            data = cform.read()
            cform.close()
        except:
            continue
        p = 12
        x1, y1, z1, x2, y2, z2 = struct.unpack('6f', data[p : p + 24])
        sizeX, sizeZ = x2 - x1, z2 - z1
        area = round(sizeX / 1000 * sizeZ / 1000, 2)
        print('{: <23} {: <4} x {: <4} = {: <4} km^2'.format(
        level, int(round(sizeX, 2)), int(round(sizeZ, 2)), area), file=log)
log.close()
print('total time: {}s'.format(time.time() - startTime))
input()