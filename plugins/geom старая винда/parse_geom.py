from stalker_tools import xray_utils, xray_import
from stalker_tools.xray_utils import unpack_data as u
from stalker_tools.xray_utils import parse_string_nul as ps
import time

st = time.time()

def parse_header(s, dump=False):
    (xrlc_version, xlrc_quality), p = u('HH', s, 0)
    if dump:
        print('  xrLC Version: {}'.format(xrlc_version))
        print('  xrLC Quality: {}'.format(xlrc_quality))


def parse_swis(s):
    p = 0
    if len(s) > 8:
        reserved, p = u('4I', s, p)
        count, p = u('I', s, p)
        for i in range(1):
            (offset, num_tris, num_verts), p = u('iHH', s, p)
        return offset // 3
    else:
        return 0


def parse_ib(s):
    ib_count, p = u('I', s, 0)
    ib = []
    for i in range(ib_count):
        indices = []
        index_count, p = u('I', s, p)
        for j in range(index_count // 3):
            (V1, V3, V2), p = u('3H', s, p)
            indices.append((V1, V2, V3))
        ib.append(indices)
    return ib


def parse_vb(s):
    vb_cnt, p = u('I', s, 0)
    vb = []
    for i in range(vb_cnt):
        p += 56
        vertex_count, p = u('I', s, p)
        vertices = []
        uvs = []
        uvs_l = []
        for i in range(vertex_count):
            (X, Z, Y), p = u('3f', s, p)
            vertices.append((X, Y, Z))
            p += 12
            (U, V), p = u('hh', s, p)
            (UL, VL), p = u('hh', s, p)
            uvs.append((U / 1024, 1 - V / 1024))
            uvs_l.append((UL / 1024, 1 - VL / 1024))
        vb.append((vertices, uvs, uvs_l))
    return vb


def parse_gcontainer(s):
    (vb_set, v_base, v_cnt, ib_set, i_base, i_cnt), p = u('6I', s, 0)
    vertices = vb[vb_set][0][v_base : v_base + v_cnt]
    uvs = vb[vb_set][1][v_base : v_base + v_cnt]
    triangles = ib[ib_set][i_base//3 : i_base//3 + i_cnt//3]
    return vertices, triangles, uvs


def parse_visual(s,):
    p = 0
    offset, vertices, triangles, uvs = 0, None, None, None
    while p < len(s):
        (id, cmpr, sz), p = u('HHI', s, p)
        if id == 0x1:
            pass
        elif id == 0x6:
            offset = parse_swis(s[p : p + sz])
        elif id == 0xa:
            pass
        elif id == 0x15:
            vertices, triangles, uvs = parse_gcontainer(s[p : p + sz])
            xray_utils.print_bytes(s[p : p + sz], out_path='c:\\LOG.TXT')
        elif id == 0x16:
            pass
        else:
            pass
        p += sz
    if offset:
        triangles = triangles[offset:]
    mesh_data = {}
    mesh_data['vertices'] = vertices
    mesh_data['triangles'] = triangles
    mesh_data['uvs'] = uvs
    mesh_data['materials'] = None
    mesh_data['images'] = None
    mesh_data['material_indices'] = None
    if vertices:
        xray_import.crete_mesh(mesh_data)


def parse_visuals(s):
    p = 0
    while p < len(s):
        (id, cmpr, sz), p = u('HHI', s, p)
        parse_visual(s[p : p + sz])
        p += sz


def parse_materials(s):
    p = 0
    mat_cnt, p = u('I', s, p)
    image_list = []
    materials = s[p : ].split(b'\x00')
    for material in materials:
        try:
            shader, images = material.split(b'/')
            image = str(images.split(b',')[0])[2:-1]
            image_list.append(image)
        except:
            pass
    return image_list  


s = xray_utils.read_bin_file('c:\\level.geom')
s += xray_utils.read_bin_file('c:\\level')
p = 0
while p < len(s):
    (id, cmpr, sz), p = u('HHI', s, p)
    if id == 0x1:
        parse_header(s[p : p + sz])
    elif id == 0x2:
        image_list = parse_materials(s[p : p + sz])
        materials = []
        import bpy
        for image_name in image_list:
            image = bpy.data.images.load('T:\\' + image_name + '.dds')
            texture = bpy.data.textures.new(image_name, 'IMAGE')
            texture.image = image
            mat = bpy.data.materials.new(image_name)
            mat.texture_slots.add()
            mat.texture_slots[0].texture = texture
            materials.append(mat)
    elif id == 0x3:
        parse_visuals(s[p : p + sz])
    elif id == 0x9:
        vb = parse_vb(s[p : p + sz])
    elif id == 0xa:
        ib = parse_ib(s[p : p + sz])
    else:
        pass
        # print(hex(id), sz)
    p += sz

ft = time.time()
print('total time: {}'.format(ft - st))

