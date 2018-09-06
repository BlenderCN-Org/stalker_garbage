from struct import unpack as u


def parse_0x1(s, tCnt):
    p = 0
    while p < len(s):
        unk = u('II6fI', s[p : p + 36])
        p += 36
        print(unk)


def parse_mesh(s):
    p = 0
    fmtVer, vCnt, tCnt = u('III', s[p : p + 12])
    p += 12
    bbox = u('6f', s[p : p + 24])
    p += 24
    verts, faces = [], []
    for i in range(vCnt):
        X, Y, Z = u('fff', s[p : p + 12])
        p += 12
        verts.append((X, Z, Y))
    for i in range(tCnt):
        v1, v2, v3, unknow = u('4I', s[p : p + 16])
        p += 16
        faces.append((v1, v3, v2))
    # import bpy
    # me = bpy.data.meshes.new('me')
    # ob = bpy.data.objects.new('ob', me)
    # me.from_pydata(verts, (), faces)
    # bpy.context.scene.objects.link(ob)
    # bpy.context.scene.update()
    return tCnt


f = open('build.cform', 'rb')
s = f.read()
f.close()
p = 0
while p < len(s):
    id, sz = u('II', s[p : p + 8])
    p += 8
    if id == 0x0:
        tCnt = parse_mesh(s[p : p + sz])
    elif id == 0x1:
        parse_0x1(s[p : p + sz], tCnt)
    p += sz
input()

