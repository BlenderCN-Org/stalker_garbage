import struct, read_block, parse_string, import_mesh, import_slots

def details_data_parse(details_data):
    position = 0
    
    while position < len(details_data):
        position, block_id, block_size = read_block.read_block(position, details_data)
        
        if block_id == 0x0:
            # print('header block ({0}) {1} bytes'.format(hex(block_id), block_size))
            slots_coords = parse_header(details_data[position : position + block_size], coord_y)
            # print_bytes(details_data[position : position + block_size])
            position += block_size
            import_slots.crete_slots(slots_coords)
        elif block_id == 0x1:
            # print('meshes block ({0}) {1} bytes'.format(hex(block_id), block_size))
            parse_meshes(details_data[position : position + block_size])
            position += block_size
        elif block_id == 0x2:
            # print('slots block ({0}) {1} bytes'.format(hex(block_id), block_size))
            coord_y = parse_slots(details_data[position : position + block_size])
            position += block_size
        else:
            print('unknow block ({0}) {1} bytes'.format(hex(block_id), block_size))
            position += block_size


def print_bytes(data):
    column = 1
    column_count = 8
    for data_byte in data:
        if column % column_count != 0:
            print('{0: ^5}'.format(hex(data_byte)), end = ' ')
            column += 1
        else:
            print(hex(data_byte))
            column += 1


def parse_header(data, coord_y):
    position = 0
    version, object_count, offset_x, offset_z, size_x, size_z = \
    struct.unpack('6i', data[position : position + 24])
    position += 24
    print('    version {}\n    object count {}\n    offset x {}' \
    '\n    offset z {}\n    size x {}\n    size z {}' \
    .format(version, object_count, offset_x, offset_z, size_x, size_z))
    
    slots_coords = []
    slots_count = size_x * size_z
    
    column = 0 - offset_x + size_x
    row = 1 - offset_z
    
    for slot in range(slots_count):
        if slot % size_x != 1:
            column += 1
            slots_coords.append((2*(column), 2*(row), coord_y[slot]))
        else:
            column += 1 - size_x
            row += 1
            slots_coords.append((2*(column), 2*(row), coord_y[slot]))
    return slots_coords


def parse_meshes(data):
    position = 0
    while position < len(data):
        mesh_id, mesh_size = struct.unpack('2i', data[position : position + 8])
        position += 8
        parse_mesh(data[position : position + mesh_size], mesh_id)
        position += mesh_size


def parse_mesh(data, mesh_id):
    position = 0
    print('    mesh{0:0>2}'.format(mesh_id), sep = '')
    shader, position = parse_string.parse_string(data, position)
    texture, position = parse_string.parse_string(data, position)
    print('        shader: {0}\n        texture {1}'.format(shader, texture), end = '')
    flags, min_scale, max_scale, vertices_count, indices_count = \
    struct.unpack('iffii', data[position : position + 20])
    position += 20
    print('{0}flags: {1}{0}min scale {2:.6}{0}max scale {3:.6}' \
    '{0}number vertices: {4}{0}number indices: {5}'\
    .format('\n        ', flags, min_scale, max_scale, vertices_count, indices_count))
    
    print('        vertices:')
    
    vertices = []
    uvs = []
    
    for vertex_id in range(vertices_count):
        print('            vertex{}'.format(vertex_id), end='')
        position_x, position_y, position_z, uv_x, uv_y = \
        struct.unpack('5f', data[position : position + 20])
        position += 20
        vertices.append((position_x, position_z, position_y))
        uvs.append((uv_x, 1 - uv_y))
        print('{0}position: {1:.4}, {2:.4}, {3:.4}{0}u, v: {4:.4}, {5:.4}'\
        .format('\n                ', position_x, position_y, position_z, uv_x, uv_y))
    
    print('        triangles:', end='')
    
    triangles = []
    
    for index_id in range(indices_count//3):
        index_1, index_2, index_3  = struct.unpack('3h', data[position : position + 6])
        position += 6
        triangles.append((index_1, index_3, index_2))
        print('{0}index{1}: {2}, {3}, {4}'.format('\n            ', index_id, index_1, index_2, index_3))
    
    import_mesh.crete_mesh('detail_'+str(mesh_id), vertices, uvs, triangles, 'details\\build_details')


def parse_slots(data):
    position = 0
    coord_y = []
    for slot in range(len(data)//16):
        slot_data = struct.unpack('iihhhh', data[position : position + 16])
        position += 16
        
        y_base = slot_data[0] & 0x3ff
        y_height = (slot_data[0] >> 12) & 0xff
        id0 = (slot_data[0] >> 20) & 0x3f
        id1 = (slot_data[0] >> 26) & 0x3f
        id2 = (slot_data[1]) & 0x3f
        id3 = (slot_data[1] >> 6) & 0x3f
        c_dir = (slot_data[1] >> 12) & 0xf
        c_hemi = (slot_data[1] >> 16) & 0xf
        c_r = (slot_data[1] >> 20) & 0xf
        c_g = (slot_data[1] >> 24) & 0xf
        c_b = (slot_data[1] >> 28) & 0xf
        position_y = (y_base*0.2-200)+(y_height*0.1)
        coord_y.append(position_y)
        # print('    slot', slot, sep='')
        # print('      position_y:', position_y)
        # print('      y_base:', y_base)
        # print('      y_height:', y_height)
        # print('      id0:', id0)
        # print('      id1:', id1)
        # print('      id2:', id2)
        # print('      id3:', id3)
        # print('      c_dir:', hex(c_dir))
        # print('      c_hemi:', hex(c_hemi))
        # print('      c_r:', hex(c_r))
        # print('      c_g:', hex(c_g))
        # print('      c_b:', hex(c_b))

        for i in range(2, 6):
            a0 = (slot_data[i] >> 0) & 0xf
            a1 = (slot_data[i] >> 4) & 0xf
            a2 = (slot_data[i] >> 8) & 0xf
            a3 = (slot_data[i] >> 12) & 0xf
            # print('      palette{}'.format(i-2))
            # print('        a0: {}'.format(a0))
            # print('        a1: {}'.format(a1))
            # print('        a2: {}'.format(a2))
            # print('        a3: {}'.format(a3))
    return coord_y
