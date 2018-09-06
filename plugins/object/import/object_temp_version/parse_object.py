import xray_utils
from xray_utils import unpack_data as u


def parse_main(d):
    p, block_id, block_size = xray_utils.read_block(0, d)
    if block_id == 0x7777:
        vertices, triangles = parse_object(d[p : p + block_size])
        mesh_data = {}
        mesh_data['vertices'] = vertices
        mesh_data['triangles'] = triangles
        mesh_data['uvs'] = None
        mesh_data['materials'] = None
        mesh_data['images'] = None
        mesh_data['material_indices'] = None
    else:
        print('! UNKNOW BLOCK', hex(block_id))
    return mesh_data


def parse_object(d):
    p = 0
    while p < len(d):
        p, block_id, block_size = xray_utils.read_block(p, d)
        if block_id == 0x0900:
            format_version, p = u('H', d, p)
        elif block_id == 0x0903:
            flags, p = u('I', d, p)
        elif block_id == 0x0907:
            parse_materials(d[p : p + block_size])
            p += block_size
        elif block_id == 0x0910:
            vertices, triangles = parse_meshes(d[p : p + block_size])
            p += block_size
        elif block_id == 0x0912:
            user_data, p = xray_utils.parse_string_nul(d, p)
        elif block_id == 0x0922:
            author_name, p = xray_utils.parse_string_nul(d, p)
            create_date, p = xray_utils.parse_date(d, p)
            modifer_name, p = xray_utils.parse_string_nul(d, p)
            modifer_date, p = xray_utils.parse_date(d, p)
        elif block_id == 0x0925:
            lod_reference, p = xray_utils.parse_string_nul(d, p)
        else:
            print('! UNKNOW BLOCK 0x7777-', hex(block_id), sep='')
            p += block_size
    return vertices, triangles


def parse_materials(d):
    material_count, p = u('I', d, 0)
    for i in range(material_count):
        material_name, p = xray_utils.parse_string_nul(d, p)
        engine_shader, p = xray_utils.parse_string_nul(d, p)
        compiler_shader, p = xray_utils.parse_string_nul(d, p)
        game_material, p = xray_utils.parse_string_nul(d, p)
        image_path, p = xray_utils.parse_string_nul(d, p)
        uv_map_name, p = xray_utils.parse_string_nul(d, p)
        (surface_flags, fvf, tc), p = u('III', d, p)


def parse_meshes(d):
    p = 0
    vertices, triangles = [], []
    while p < len(d):
        (mesh_id, mesh_size), p = u('II', d, p)
        curent_vert, curent_faces = parse_mesh(d[p : p + mesh_size])
        vertices.append(curent_vert)
        triangles.append(curent_faces)
        p += mesh_size
    return vertices, triangles


def parse_mesh(d):
    p = 0
    while p < len(d):
        p, block_id, block_size = xray_utils.read_block(p, d)
        if block_id == 0x1000:
            mesh_version, p = u('H', d, p)
        elif block_id == 0x1001:
            mesh_name, p = xray_utils.parse_string_nul(d, p)
        elif block_id == 0x1002:
            mesh_flags, p = u('B', d, p)
        elif block_id == 0x1004:
            bbox, p = u('6f', d, p)
        elif block_id == 0x1005:
            vertices = parse_vertices(d[p : p + block_size])
            p += block_size
        elif block_id == 0x1006:
            triangles = parse_indices(d[p : p + block_size])
            p += block_size
        elif block_id == 0x1008:
            parse_uv_indices(d[p : p + block_size])
            p += block_size
        elif block_id == 0x1009:
            parse_material_indices(d[p : p + block_size])
            p += block_size
        elif block_id == 0x1010:
            (mesh_option_0, mesh_option_1), p = u('II', d, p)
        elif block_id == 0x1012:
            parse_uvs(d[p : p + block_size])
            p += block_size
        elif block_id == 0x1013:
            smooth_groups, p = u('%dI'%(len(d[p : p + block_size])//4), d, p)
        else:
            print('! UNKNOW BLOCK 0x7777-0x0910-', hex(block_id), sep='')
            p += block_size
    return vertices, triangles


def parse_vertices(d):
    vertex_count, p = u('I', d, 0)
    vertices = []
    for i in range(vertex_count):
        (loc_x, loc_y, loc_z), p = u('3f', d, p)
        vertices.append((loc_x, loc_z, loc_y))
    return vertices


def parse_indices(d):
    triangles_count, p = u('I', d, 0)
    triangles = []
    for i in range(triangles_count):
        (vertex1, vertex2, vertex3, uv1, uv2, uv3), p = u('6I', d, p)
        triangles.append((vertex1, vertex3, vertex2))
    return triangles


def parse_uv_indices(d):
    count, p = u('I', d, 0)
    for i in range(count):
        set, p = u('B', d, p)
        vmap, p = u('4B', d, p)
        uv_index, p = u('I', d, p)


def parse_material_indices(d):
    material_count, p = u('H', d, 0)
    for i in range(material_count):
        material_name, p = xray_utils.parse_string_nul(d, p)
        triangles_count, p = u('I', d, p)
        material_indices, p = u('%dI' % triangles_count, d, p)


def parse_uvs(d):
    vmap_count, p = u('I', d, 0)
    for i in range(vmap_count):
        vmap_name, p = xray_utils.parse_string_nul(d, p)
        (value_dim, has_pidata, value_type), p = u('3B', d, p)
        data_count, p = u('I', d, p)
        for j in range(data_count):
            uv, p = u('2f', d, p)
        for j in range(data_count):
            unknow, p = u('I', d, p)


d = xray_utils.read_bin_file('1', 'object')
parse_main(d)
input()

