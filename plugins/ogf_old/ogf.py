from struct import unpack
f = open('c:\\wpn_ak74.ogf', 'rb')
s = f.read()
f.close()

try:
    import bpy
    useBlender = True
except:
    useBlender = False


def parse_vertices(s):
    p = 0
    vertFmt, vCnt = unpack('II', s[p : p + 8])
    p += 8
    verts, vertsIndices, index = [], {}, 0
    for i in range(vCnt):
        X, Y, Z, normX, normY, normZ, U, V, matrix = unpack('8fi', s[p : p + 36])
        p += 36
        if not [X, Z, Y] in verts:
            verts.append([X, Z, Y])
            vertsIndices[i] = index
            index += 1
        else:
            vertsIndices[i] = verts.index([X, Z, Y])
    print(len(verts), len(vertsIndices))
    return verts, vertsIndices


def parse_indices(s, verts, vertsIndices):
    p = 0
    iCnt = unpack('I', s[p : p + 4])[0]
    p += 4
    triangles = []
    for i in range(iCnt // 3):
        v1, v2, v3 = unpack('HHH', s[p : p + 6])
        p += 6
        v1 = vertsIndices[v1]
        v2 = vertsIndices[v2]
        v3 = vertsIndices[v3]
        triangles.append([v1, v3, v2])
    return triangles


def parse_children(s):
    p = 0
    while p < len(s):
        id, size = unpack('II', s[p : p + 8])
        p += 8
        if id == 0x7:
            verts, vertsIndices = parse_vertices(s[p : p + size])
        elif id == 0x8:
            triangles = parse_indices(s[p : p + size], verts, vertsIndices)
        p += size
    if useBlender:
        me = bpy.data.meshes.new('OGF_v3')
        me.from_pydata(verts, (), triangles)
        ob = bpy.data.objects.new('OGF_v3', me)
        bpy.context.scene.objects.link(ob)


def parse_childrens(s):
    p = 0
    while p < len(s):
        id, size = unpack('II', s[p : p + 8])
        p += 8
        parse_children(s[p : p + size])
        p += size


p = 0
while p < len(s):
    id, compress, size = unpack('HHI', s[p : p + 8])
    p += 8
    if id == 0x11:
        parse_childrens(s[p : p + size])
    else:
        pass
        # print(hex(id), compress, size)
    p += size

if not useBlender:
    input()