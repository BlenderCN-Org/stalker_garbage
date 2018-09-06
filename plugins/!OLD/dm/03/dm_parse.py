import struct, utils
from utils import unpack_data as u


def parse_main(dm_data):
    position = 0
    shader_name, position = utils.parse_string_nul(dm_data, position)
    texture_name, position = utils.parse_string_nul(dm_data, position)
    dm_info, position = u('IffII', dm_data, position)
    flags, min_scale, max_scale, vertex_count, index_count = dm_info
    
    vertices = []
    uvs = []
    for vertex_id in range(vertex_count):
        vertex, position = u('5f', dm_data, position)
        loc_x, loc_y, loc_z, uv_x, uv_y = vertex
        vertices.append((loc_x, loc_z, loc_y))
        uvs.append((uv_x, 1 - uv_y))
    
    triangles = []
    for index_id in range(index_count//3):
        face, position = u('3H', dm_data, position)
        index_1, index_2, index_3 = face
        triangles.append((index_1, index_3, index_2))
    return vertices, uvs, triangles, texture_name

