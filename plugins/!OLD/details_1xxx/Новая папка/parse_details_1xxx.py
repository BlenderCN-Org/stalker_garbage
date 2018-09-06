from stalker_tools import xray_utils, xray_import
from stalker_tools.xray_utils import unpack_data as u
from stalker_tools.xray_utils import parse_string_nul as ps
# import bpy


def parse_header(s):
    (ver, ob_cnt, ofx, ofz, szx, szz), p = u('IIiiII', s, 0)
    # print('  version format:', hex(ver))
    # print('  mesh count:', ob_cnt)
    # print('  slots offset: ({}, {})'.format(ofx, ofz))
    # print('  slots size:   ({}, {})'.format(szx, szz))


def parse_meshes(s):
    p = 0
    while p < len(s):
        (id, size), p = u('II', s, p)
        # print('  mesh{:0>2}, size: {}'.format(id, size))
        parse_mesh(s[p : p + size])
        p += size


def parse_mesh(s):
    p = 0
    shr, p = ps(s, p)
    txr, p = ps(s, p)
    (flg, min, max, vcnt, icnt), p = u('IffII', s, p)
    # print('  shader: {}, image: {}'.format(shr, txr))
    # print('  vertices: {}, indices: {}\n'.format(vcnt, icnt))
    verts = []
    uvs = []
    for v in range(vcnt):
        (X, Z, Y), p = u('fff', s, p)
        (U, V), p = u('ff', s, p)
        verts.append((X, Y, Z))
        uvs.append((U, 1 - V))
    indices = []
    for t in range(icnt // 3):
        tri, p = u('3H', s, p)
        indices.append((tri[0], tri[2], tri[1]))
    mesh_data = {}
    mesh_data['vertices'] = verts
    mesh_data['triangles'] = indices
    mesh_data['uvs'] = uvs
    mesh_data['images'] = txr
    mesh_data['material_indices'] = None
    mesh_data['materials'] = None
    xray_import.crete_mesh(mesh_data)


def parse_slots(s):
    p = 0
    slot_count = len(s) // 22
    for i in range(slot_count):
        (y_base, y_height), p = u('ff', s, p)
        id0,  p = u('B', s, p)
        clr0, p = u('H', s, p)
        id1,  p = u('B', s, p)
        clr1, p = u('H', s, p)
        id2,  p = u('B', s, p)
        clr2, p = u('H', s, p)
        id3,  p = u('B', s, p)
        clr3, p = u('H', s, p)
        unk,  p = u('H', s, p)


s = xray_utils.read_bin_file('c:\\level.details')
p = 0
while p < len(s):
    (id, unk, size), p = u('HHI', s, p)
    if id == 0x0:
        pass
        # print('header ({}), size: {}'.format(hex(id), size))
        # parse_header(s[p : p + size])
    elif id == 0x1:
        # print('meshes ({}), size: {}'.format(hex(id), size))
        parse_meshes(s[p : p + size])
    elif id == 0x2:
        pass
        # print('slots ({}), size: {}'.format(hex(id), size))
        # parse_slots(s[p : p + size])
    else:
        print('! UNKNOWN BLOCK {: <3} {: <5} {}'.format(hex(id), unk, size))
    p += size

# for n, ob in enumerate(bpy.context.scene.objects):
    # ob.location.x = n

