from struct import *
f = open('1.object', 'rb')
s = f.read()
f.close()

p = 0
block_id = unpack('i', s[p : p + 4])[0]
p += 4
block_size = unpack('i', s[p : p + 4])[0]
p += 4
print('\nblock id = %s,\tblock size = %s\n' % (hex(block_id), block_size))
print('OBJECT FILE:\n')
while p < len(s):
	block_id = unpack('i', s[p : p + 4])[0]
	p += 4
	block_size = unpack('i', s[p : p + 4])[0]
	p += 4
	print('\nblock id = %s,\tblock size = %s\n' % (hex(block_id), block_size))
	# print(s[p : p + block_size])
	p += block_size
input()
