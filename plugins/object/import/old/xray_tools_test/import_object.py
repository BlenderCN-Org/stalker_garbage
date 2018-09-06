import time, file_size
from unpack_data import *

start_time = time.time()
f = open('1.object', 'rb')
s = f.read()
f.close()
file_size.calc_file_size(s)

header = u(s, 'i', o2)
print('main block = {0}'.format(header))
data_size = u(s, 'i', o1)
print('data size {0} = {1}'.format(header, data_size))

block_id = 'TEMP'

while block_id != None:
    block_id = u(s, 'i', o2)
    if block_id == None:
        break
    block_size = u(s, 'i', o4)
    print('Block', block_id)

finish_time = time.time()
print('Time:', finish_time - start_time)
input()