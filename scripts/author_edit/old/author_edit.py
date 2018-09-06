"""

Скрипт изменяет автора в файле *.object

"""


from struct import *
f = open(r'1.object', 'rb')
s = f.read()
file_size = len(s) - 8
f.close()

def return_time(s):
    p = 0
    ch = unpack('s', s[p : p + 1])[0]
    p += 1
    author = ''
    while ch != b'\x00':
        author += str(ch)[2:-1]
        ch = unpack('s', s[p : p + 1])[0]
        p += 1
    date_1 = s[p : p + 4]
    p += 4
    ch = unpack('s', s[p : p + 1])[0]
    p += 1
    modifer = ''
    while ch != b'\x00':
        modifer += str(ch)[2:-1]
        ch = unpack('s', s[p : p + 1])[0]
        p += 1
    date_2 = s[p : p + 4]
    return  date_1, date_2

p = 8
while p < len(s):
    block_id = unpack('i', s[p : p + 4])[0]
    p += 4
    block_size = unpack('i', s[p : p + 4])[0]
    p += 4

    if block_id == 0x922:

        data = s[p : p + block_size]
        new_author = b'\\\\COMP\\Pavel_Blend'
        new_modifer = b'Python 3.3.5.'
        
        date_1, date_2 = return_time(data)
        
        new_block = new_author+b'\x00'+date_1+new_modifer+b'\x00'+date_2
        new_size = len(new_author) + 4 + len(new_modifer) + 4 + 2
        
        new_file_size = file_size - block_size + new_size
        
        new_file = s[0 : 4]
        new_file += pack('i', new_file_size)
        new_file += s[8 : p - 4]
        new_file += pack('i', new_size)
        new_file += new_block
        
        save_f = open('new.object', 'wb')
        save_f.write(new_file)
        save_f.close()

    p += block_size
print('new author:', str(new_author)[2:-1])
input('press enter')
