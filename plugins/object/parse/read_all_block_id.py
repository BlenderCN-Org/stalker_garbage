from struct import *
f = open('stalker_hood.object', 'rb')
s = f.read()
f.close()

def parse_mesh(s):
    p = 0
    while p < len(s):
        
        block_id = unpack('i', s[p : p + 4])[0]
        p += 4
        
        block_size = unpack('i', s[p : p + 4])[0]
        p += 4
        
        print('\n  block id = %s,\tblock size = %s' % (hex(block_id), block_size))
        
        while p < len(s):
            block_id = unpack('i', s[p : p + 4])[0]
            p += 4
            
            block_size = unpack('i', s[p : p + 4])[0]
            p += 4
            
            p += block_size
            
            print('\n    block id = %s,\tblock size = %s' % (hex(block_id), block_size))
            
        p += block_size - 8

p = 0
block_id = unpack('i', s[p : p + 4])[0]
p += 4
block_size = unpack('i', s[p : p + 4])[0]
p += 4
print('\nblock id = %s,\tblock size = %s' % (hex(block_id), block_size))

while p < len(s):
    block_id = unpack('i', s[p : p + 4])[0]
    p += 4
    block_size = unpack('i', s[p : p + 4])[0]
    p += 4
    print('\nblock id = %s,\tblock size = %s' % (hex(block_id), block_size))
    if block_id == 0x910:
        parse_mesh(s[p : p + block_size])
    p += block_size
input()
