from struct import unpack

f = open('scene_object.part', 'rb')
s = f.read()
f.close()

save_file = open('references.txt', 'w')

#print(unpack('%ds' % (len(s)), s)[0])

def u(p):
    return unpack('b', s[p : p + 1])[0], p + 1

scene_objects = {}
references = {}
path = 'X:\\\\rawdata\\\\objects\\\\'
p = 0
block_id = None

while p < len(s):
    block_id, p = u(p)
    if block_id == 6:
        block_id, p = u(p)
        if block_id == -7:
            p += 2
            name_size = unpack('i', s[p : p + 4])[0]
            p += 4
            name = unpack('%ds' % (name_size), s[p : p + name_size])[0]
            name = str(name)[2:-5]
            scene_objects[name] = True
            p += name_size
    elif block_id == 3:
        block_id, p = u(p)
        if block_id == -7:
            p += 2
            p += 40
            p += 26
            name_reference = ''
            ch = unpack('s', s[p : p + 1])[0]
            p += 1
            while ch != b'\x00':
                name_reference += str(ch)[2:-1]
                ch = unpack('s', s[p : p + 1])[0]
                p += 1
            references[path + name_reference] = True

for i in references.keys():
    print(i, file = save_file)

save_file.close()

input('\nPress Enter')