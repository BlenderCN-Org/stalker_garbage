import struct, bpy
f = open('c:\\scene_object.part', 'rb')
s = f.read()
f.close()


def parse_object_data(s):
    p = 0
    bbox = struct.unpack('6f', s[p : p + 24])
    p += 24
    options = struct.unpack('HH', s[p : p + 4])
    p += 4
    status = struct.unpack('HH', s[p : p + 4])
    p += 4
    unknow = struct.unpack('4B', s[p : p + 4])
    p += 4
    name_size = struct.unpack('I', s[p : p + 4])[0]
    p += 4
    name = struct.unpack('%ds' % name_size, s[p : p + name_size])[0]
    p += name_size
    unknow = struct.unpack('2I', s[p : p + 8])
    p += 8
    loc = struct.unpack('3f', s[p : p + 12])
    p += 12
    # print(loc)
    rot = struct.unpack('3f', s[p : p + 12])
    p += 12
    scale = struct.unpack('3f', s[p : p + 12])
    p += 12
    p += 26
    name_mesh = ''
    b = struct.unpack('B', s[p : p + 1])[0]
    p += 1
    while b != 0:
        name_mesh += chr(b)
        b = struct.unpack('B', s[p : p + 1])[0]
        p += 1
    name = name_mesh
    # name = name_mesh.split('\\')[-1]
    return name, (loc[0], loc[2], loc[1]), (rot[0], rot[2], rot[1]), (scale[0], scale[2], scale[1])


def parse_7000(s):
    pass


def parse_0003(s):
    p = 0
    names = {}
    while p < len(s):
        object_id = struct.unpack('I', s[p : p + 4])[0]
        p += 4
        object_size = struct.unpack('I', s[p : p + 4])[0]
        p += 4
        object_data = s[p : p + object_size]
        name, loc, rot, scl = parse_object_data(object_data)
        names[name] = True
        try:
            me = bpy.data.meshes[name]
        except:
            me = None
        p += object_size
        ob = bpy.data.objects.new('ob', me)
        bpy.context.scene.objects.link(ob)
        ob.location = loc
        ob.rotation_euler = rot
        ob.scale = scl
    names = list(names.keys())
    names.sort()
    save = open('c:\\object_list.txt', 'w')
    for i in names:
        print(i, file=save)
    save.close()


def parse_8002(s):
    p = 0
    while p < len(s):
        block = struct.unpack('I', s[p : p + 4])[0]
        p += 4
        size = struct.unpack('I', s[p : p + 4])[0]
        p += 4
        # print('  id = {0} size = {1}'.format(hex(block), size))
        if block == 0x7777:
            pass
        elif block == 0x0002:
            pass
        elif block == 0x0003:
            parse_0003(s[p : p + size])
        elif block == 0x1001:
            pass
        elif block == 0x1003:
            pass
        elif block == 0x1002:
            pass
        p += size


p = 0
while p < len(s):
    block = struct.unpack('I', s[p : p + 4])[0]
    p += 4
    size = struct.unpack('I', s[p : p + 4])[0]
    p += 4
    # print('id = {0} size = {1}'.format(hex(block), size))
    if block == 0x7000:
        parse_7000(s[p : p + size])
    elif block == 0x8002:
        parse_8002(s[p : p + size])
    p += size

