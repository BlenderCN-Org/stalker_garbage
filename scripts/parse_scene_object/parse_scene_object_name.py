from struct import unpack

f = open('scene_object.part', 'rb')
s = f.read()
f.close()

def u(p):
    return unpack('b', s[p : p + 1])[0], p + 1

scene_objects = {}
p = 0
block_id = None

while p < len(s):
    block_id, p = u(p)
    if block_id == 7:
        block_id, p = u(p)
        if block_id == -7:
            p += 2
            name_size = unpack('i', s[p : p + 4])[0]
            p += 4
            name = unpack('%ds' % (name_size), s[p : p + name_size])[0]
            name = str(name)[2:-5]
            scene_objects[name] = True

print('objects count: %i\n' % (len(scene_objects)))

for i in scene_objects.keys():
    print(i)

input('\nPress Enter')