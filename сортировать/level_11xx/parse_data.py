import struct, parse_string


def parse_header(data):
    print('HEADER 0x01')
    position = 0
    xrlc_version, xrlc_quality = struct.unpack('HH', data[position : position + 4])
    position += 4
    print('  xrlc_version: {}'.format(xrlc_version))
    print('  xrlc_quality: {}'.format(xrlc_quality))
    name = ''
    c = struct.unpack('b', data[position : position + 1])[0]
    position += 1
    while c != 0:
        name += chr(c)
        c = struct.unpack('b', data[position : position + 1])[0]
        position += 1
    print('  name: {}'.format(name))


def parse_shaders(data):
    print('SHADERS 0x02')
    position = 0
    shader_count = struct.unpack('I', data[position : position + 4])[0]
    position += 4
    print('  shader_count:', shader_count)
    for i in range(shader_count):
        shaders, position = parse_string.parse_string(data, position)
        print(' ', shaders)

def parse_vertices(data):
    print('VERTICES 0x03')
    position = 0
    unknown = struct.unpack('4B', data[position : position + 4])
    position += 4
    print('  unknown: {0}'.format(unknown))
    vertices = []
    
    for i in range(len(data[position:]) // 12):
        vertex = struct.unpack('3f', data[position : position + 12])
        position += 12
        vertices.append(vertex)
        # print(vertex)
    return vertices

