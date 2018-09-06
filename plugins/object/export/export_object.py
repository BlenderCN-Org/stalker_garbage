from struct import pack, unpack

version_block = pack('iih', 0x0900, 2, 0x10)
user_data_block = pack('iib', 0x0912, 1, 0)
lod_ref_block = pack('iib', 0x0925, 1, 0)
flags_block = pack('3i', 0x0903, 4, 0)
authors = pack('b', 0) * 46
author_block = pack('ii', 0x0922, len(authors)) + authors

f = open(r'c:\1.object', 'rb')
s = f.read()
f.close()
p = 8
file_size = len(s)
while p < file_size:
    block, size = unpack('2i', s[p : p + 8])
    p += 8
    if block == 0x0910:
        geom = s[p - 8: p + size]
    elif block == 0x0907:
        mat = s[p - 8: p + size]
    p += size
    

data=version_block+user_data_block+lod_ref_block+flags_block+geom+mat+author_block
header_block = pack('2i', 0x7777, len(data))
new_object = open(r'c:\new.object', 'wb')
new_object.write(header_block)
new_object.write(data)
input('finish')