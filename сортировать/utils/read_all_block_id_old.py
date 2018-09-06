from struct import *
f = open('1.object', 'rb')
s = f.read()
f.close()

def print_bytes(bytes):
    data = unpack('%db' % len(bytes), bytes)
    data = list(map(hex, data))
    t = 0
    for i in data:
        t += 1
        if t % 8 == 0:
            print(i, end='\n')
        else:
            print(i, end='\t')

def search_chunk(data, id, out = False):
    p = 0
    while p < len(data):
        block_id = unpack('i', data[p : p + 4])[0]
        p += 4
        block_size = unpack('i', data[p : p + 4])[0]
        p += 4
        if block_id == id:
            if out == True:
                print('\nblock id = %s,\tblock size = %s\n' % (hex(block_id), block_size))
            return data[p : p + block_size]
        p += block_size

data = search_chunk(s[8:], 0x0910, False)
#print_bytes(s[p : p + size])
data = search_chunk(data[8:], 0x1008, True)
print_bytes(data)
input()