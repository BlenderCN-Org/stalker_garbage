import struct, ogf_format, parse_string, import_mesh


def ogf_data_parse(data):
    try:
        import bpy
        use_blender = True
    except:
        use_blender = False
    data_size = len(data)
    position = 0
    while position < data_size:
        block_id, block_size = struct.unpack('ii', data[position : position + 8])
        position += 8
        if block_id == ogf_format.HEADER[0]:
            print(ogf_format.HEADER[1], ogf_format.HEADER[0])
            parse_header(data[position : position + block_size])
        elif block_id == ogf_format.TEXTURE[0]:
            print(ogf_format.TEXTURE[1], ogf_format.TEXTURE[0])
            texture_name = parse_texture(data[position : position + block_size])
        elif block_id == ogf_format.VERTICES[0]:
            print(ogf_format.VERTICES[1], ogf_format.VERTICES[0])
            vertices, uvs = parse_vertices(data[position : position + block_size])
        elif block_id == ogf_format.INDICES[0]:
            print(ogf_format.INDICES[1], ogf_format.INDICES[0])
            triangles = parse_indices(data[position : position + block_size])
        elif block_id == ogf_format.CHILDREN[0]:
            print(ogf_format.CHILDREN[1], ogf_format.CHILDREN[0])
            parse_childrens(data[position : position + block_size])
        else:
            print('block {0:>2}, size = {1}'.format(hex(block_id), block_size))
        position += block_size
    #if use_blender:
        #import_mesh.crete_mesh('ogf', vertices, uvs, triangles, texture_name)


def parse_header(data):
    position = 0
    
    format_version = struct.unpack('b', data[position : position + 1])[0]
    position += 1
    print('  format version:', format_version)
    
    mesh_type = struct.unpack('b', data[position : position + 1])[0]
    position += 1
    print('  mesh type:', ogf_format.mesh_type_names[mesh_type])
    
    shader_id = struct.unpack('h', data[position : position + 2])[0]
    position += 2
    print('  shader id:', shader_id)
    
    bbox = struct.unpack('6f', data[position : position + 24])
    position += 24
    print('  bbox:')
    print('    {0: >6.3}, {1: >6.3}, {2: >6.3}\n    {3: >6.3}, {4: >6.3}, {5: >6.3}'.format(
    bbox[0], bbox[1], bbox[2], bbox[3], bbox[4], bbox[5]))
    
    bsphere = struct.unpack('4f', data[position : position + 16])
    position += 16
    print('  bsphere:\n    radius: {0: >6.3}, {1: >6.3}, {2: >6.3}\n    center: {3: >6.3}'.format(
    bsphere[0], bsphere[1], bsphere[2], bsphere[3]))


def parse_texture(data):
    position = 0
    texture_name, position = parse_string.parse_string(data, position)
    shader_name, position = parse_string.parse_string(data, position)
    print('  texture name:', texture_name)
    print('  shader  name:', shader_name)
    return texture_name


def parse_vertices(data):
    position = 0
    vertex_format, vertex_count = struct.unpack('2i', data[position : position + 8])
    position += 8
    print('  vertex format:', hex(vertex_format))
    print('  vertex  count:', vertex_count)
    
    vertices = []
    uvs = []
    
    if vertex_format == ogf_format.vertex_format['OLD']:
        for i in range(vertex_count):
            vertex_data = struct.unpack('8f', data[position : position + 32])
            position += 32
            vertices.append((vertex_data[0], vertex_data[2], vertex_data[1]))
            uvs.append((vertex_data[6], 1 - vertex_data[7]))
    elif vertex_format == ogf_format.vertex_format['1L'] or vertex_format == 1:
        for i in range(vertex_count):
            vertex_data = struct.unpack('14fi', data[position : position + 60])
            position += 60
            
            vertices.append((vertex_data[0], vertex_data[2], vertex_data[1]))
            # normal = vertex_data[3:6]
            # t = vertex_data[6:9]
            # b = vertex_data[9:12]
            uvs.append((vertex_data[12], 1 - vertex_data[13]))
            # matrix = vertex_data[14]
    elif vertex_format == ogf_format.vertex_format['2L'] or vertex_format == 2:
        for i in range(vertex_count):
            vertex_data = struct.unpack('2h15f', data[position : position + 64])
            position += 64
            
            vertices.append((vertex_data[2], vertex_data[3], vertex_data[4]))
            uvs.append((vertex_data[15], 1 - vertex_data[16]))
        
    return vertices, uvs


def parse_indices(data):
    position = 0
    indices_count = struct.unpack('i', data[position : position + 4])[0]
    position += 4
    print('  indices count =', indices_count)
    triangles = []
    
    for i in range(indices_count // 3):
        triangle = struct.unpack('3h', data[position : position + 6])
        position += 6
        triangles.append((triangle[0], triangle[2], triangle[1]))
    return triangles


def parse_childrens(data):
    position = 0
    
    while position < len(data):
        mesh_id, mesh_size = struct.unpack('2i', data[position : position + 8])
        position += 8
        parse_children(data[position : position + mesh_size])
        position += mesh_size


def parse_children(data):
    try:
        import bpy
        use_blender = True
    except:
        use_blender = False
    
    position = 0
    while position < len(data):
        block_id, block_size = struct.unpack('ii', data[position : position + 8])
        position += 8
        if block_id == ogf_format.HEADER[0]:
            print(ogf_format.HEADER[1], ogf_format.HEADER[0])
            parse_header(data[position : position + block_size])
        elif block_id == ogf_format.TEXTURE[0]:
            print(ogf_format.TEXTURE[1], ogf_format.TEXTURE[0])
            texture_name = parse_texture(data[position : position + block_size])
        elif block_id == ogf_format.VERTICES[0]:
            print(ogf_format.VERTICES[1], ogf_format.VERTICES[0])
            vertices, uvs = parse_vertices(data[position : position + block_size])
        elif block_id == ogf_format.INDICES[0]:
            print(ogf_format.INDICES[1], ogf_format.INDICES[0])
            triangles = parse_indices(data[position : position + block_size])
        else:
            print('  block {0:>2}, size = {1}'.format(hex(block_id), block_size))
        position += block_size
    if use_blender:
        import_mesh.crete_mesh('ogf', vertices, uvs, triangles, texture_name)
