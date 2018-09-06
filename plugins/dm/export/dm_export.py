import bpy, struct, export_uv

mesh = bpy.context.object.data

export_file = open('c:\\test.dm', 'wb')
shader = 'default'
export_file.write(struct.pack('%ds' % (len(shader) + 1), bytes(shader, encoding='utf-8')))
texture = 'terrain\\terrain_agroprom'
export_file.write(struct.pack('%ds' % (len(texture) + 1), bytes(texture, encoding='utf-8')))
flags = 0
export_file.write(struct.pack('i', flags))
min_size = 0.8
max_size = 1.2
export_file.write(struct.pack('2f', min_size, max_size))
vertex_count = (len(mesh.vertices))
face_count = (len(mesh.polygons))
export_file.write(struct.pack('2i', vertex_count, face_count * 3))

vertices = []
uvs = export_uv.export_uv(mesh)

for vertex in range(vertex_count):
    vertices.extend((
    mesh.vertices[vertex].co[0], mesh.vertices[vertex].co[1], mesh.vertices[vertex].co[2]))
    vertices.extend((mesh.uv_layers[0].data[vertex].uv[0], mesh.uv_layers[0].data[vertex].uv[1]))

print(len(vertices), len(uvs))

indices = []

for index in range(face_count):
    indices.extend((
    mesh.polygons[index].vertices[0], mesh.polygons[index].vertices[1], mesh.polygons[index].vertices[2]))

for vertex in vertices:
    export_file.write(struct.pack('f', vertex))

for index in indices:
    export_file.write(struct.pack('h', index))

export_file.close()

