from struct import *


def parse_vertices(s):
    p = 0
    vertex_block_count = unpack('I', s[p : p + 4])[0]
    p += 4
    
    vertices_buffer = {}
    
    for i in range(vertex_block_count):
        start_new_block = unpack('I', s[p : p + 4])[0]
        p += 4
        start_format_vertex = unpack('I', s[p : p + 4])[0]
        p += 4
        vertex_format = unpack('4H', s[p : p + 8])
        p += 8
        unknow = s[p : p + 32]
        p += 32
        end_format_vertex = unpack('I', s[p : p + 4])[0]
        p += 4
        start_vertex = unpack('I', s[p : p + 4])[0]
        p += 4
        vertex_count = unpack('I', s[p : p + 4])[0]
        p += 4
        vertices = []
        uvs = []
        
        for j in range(vertex_count):
            coord = unpack('3f', s[p : p + 12])
            p += 12
            vertices.append(coord)
            normal = unpack('3b', s[p : p + 3])
            p += 3
            light_factor = unpack('B', s[p : p + 1])[0]
            p += 1
            tangent = unpack('3b', s[p : p + 3])
            p += 3
            corector_uv_x = unpack('b', s[p : p + 1])[0]
            p += 1
            bi_tangent = unpack('3b', s[p : p + 3])
            p += 3
            corector_uv_y = unpack('b', s[p : p + 1])[0]
            p += 1
            uv = unpack('2f', s[p : p + 8])
            p += 8
            uvs.append(uv)
        vertices_buffer[i] = vertices
    return vertices_buffer


def parse_indices(s):
    p = 0
    index_block_count = unpack('I', s[p : p + 4])[0]
    p += 4
    indices_buffer = {}
    
    for i in range(index_block_count):
        index_count = unpack('I', s[p : p + 4])[0]
        p += 4
        faces = []
        
        for j in range(index_count//3):
            i1, i2, i3 = unpack('3H', s[p : p + 6])
            faces.append([i1, i2, i3])
            p += 6
        indices_buffer[i] = faces
    return indices_buffer


def parse_geom(s):
    p = 0
    
    while p < len(s):
        block_id, compress, block_size = unpack('2HI', s[p : p + 8])
        p += 8
        
        if block_id == 9:
            vertices_buffer = parse_vertices(s[p : p + block_size])
        elif block_id == 10:
            indices_buffer = parse_indices(s[p : p + block_size])
        p += block_size
    return vertices_buffer, indices_buffer

