from struct import unpack
from time import ctime

f = open('1.object', 'rb')
s = f.read()
f.close()

def parse_string(s, p):
    string = ''
    ch = unpack('b', s[p : p + 1])[0]
    p += 1
    while ch != 0:
        string += chr(ch)
        ch = unpack('b', s[p : p + 1])[0]
        p += 1
    return string, p

def parse_date(s, p):
    date = ctime(unpack('i', s[p : p + 4])[0])
    p += 4
    return date, p

p = 0

block_id = unpack('i', s[p : p + 4])[0]     # MAIN 0x7777
p += 4

block_size = unpack('i', s[p : p + 4])[0]
p += 4

while p < len(s):
    block_id = unpack('i', s[p : p + 4])[0]
    p += 4
    
    block_size = unpack('i', s[p : p + 4])[0]
    p += 4
    
    if block_id == 0x922:
        author_name, p = parse_string(s, p)
        print('Owner Name %s' % author_name)
        
        create_date, p = parse_date(s, p)
        print('Creation Time %s' % create_date, end = '\n'*2)
        
        edit_name, p = parse_string(s, p)
        print('Modif Name %s' % edit_name)
        
        edit_date, p = parse_date(s, p)
        print('Modifed Time %s' % edit_date, end = '\n'*2)
    
    p += block_size

input()