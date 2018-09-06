from struct import unpack

geom_file = open(r'level.geom', 'rb')
s = geom_file.read()
geom_file.close()

file_size = len(s)

p = 0
print('='*79)

while p < file_size:
    
    block_id = unpack('i', s[p : p + 4])[0]
    p += 4
    
    block_size = unpack('i', s[p : p + 4])[0]
    p += 4
    
    if block_id == 9 or block_id == 10:
        print('block id', block_id)
        print('block size', block_size)
        print('='*79)
    
    if block_id == 9:
        vertices_file = open(r'c:\vertices.bin', 'wb')
        vertices_file.write(s[p : p + block_size])
        vertices_file.close()

    
    if block_id == 10:
        '''
        indices_file = open(r'c:\faces.bin', 'wb')
        indices_file.write(s[p : p + block_size])
        indices_file.close()
        '''
        
        indices_block_count = unpack('i', s[p : p + 4])[0]
        p += 4
        
        surface_count = 0
        
        for i in range(indices_block_count):
            indices_count = unpack('i', s[p : p + 4])[0]
            p += 4
            
            for i in range(indices_count):
                index = unpack('h', s[p : p + 2])[0]
                p += 2
                print('\tindex%d' % i, index)
    
    p += block_size

input('Finish')