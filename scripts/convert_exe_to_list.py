f = open('lzhuf.exe', 'rb')
s = f.read()
f.close()

from xray_utils import unpack_data as u


p = 0
code = []
fileSize = len(s)
while p < fileSize:
    (b, ), p = u('B', s, p)
    code.append(b)

f = open('bin_code.py', 'w')
c = 3
for i in code:
    if c % 16 != 0:
        f.write('{0: >3}, '.format(i))
    else:
        f.write('{0: >3},\n'.format(i))
    c += 1
f.close()

input()