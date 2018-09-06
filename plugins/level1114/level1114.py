from struct import unpack
f = open('level', 'rb')
s = f.read()
f.close()
p = 0
chunks = {
0x1 : 'HEADER',
0x2 : 'SHADERS',
0x3 : 'VISUALS',
0x4 : 'VB',
0x5 : 'CFORM',
0x6 : 'PORTALS',
0x7 : 'LIGHTS',
0x9 : 'GLOWS',
0xa : 'SECTORS'}
print('-' * 40)
print('- name    - id  - compress - size      -')
print('-' * 40)
while p < len(s):
    id, compress, size = unpack('HHI', s[p : p + 8])
    p += 8
    print('- {0: <7} - {1: <3} - {2} - {3: <10}-'.format(chunks[id], hex(id), '{: <8}'.format(str(bool(compress))), size))
    p += size
print('-' * 40)
input()