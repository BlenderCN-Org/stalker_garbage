import bpy
from struct import pack

version = pack('iih', 0x1000, 2, 0x10)

ob = bpy.context.active_object
name_size = len(ob.name)
name = pack('2i', 0x1001, name_size)
name += pack('5s', b'test')

bbox = pack('2i6f', 0x1004, 24, 1, 1, 1, 1, 1, 1)

flags = pack('2ih', 0x1002, 1, 0x5)

option = pack('4i', 0x1008, 8, 0, 0)

me = ob.data
vert_count = len(me.vertices)
verts = pack('3i', 0x1005, vert_count*4*3+4, vert_count)

for i in range(vert_count):
    verts += pack('3f', me.vertices[i].co[0], me.vertices[i].co[1], me.vertices[i].co[2])

face_count = len(me.polygons)
print(face_count)
faces = pack('2i', 0x1006, face_count)

for i in range(face_count):
    faces += pack('6i', me.polygons[i].vertices[0], me.polygons[i].vertices[0], me.polygons[i].vertices[1], me.polygons[i].vertices[1], me.polygons[i].vertices[2], me.polygons[i].vertices[2])

smooth = pack('2i', 0x1013, face_count*4)

for i in range(face_count):
    smooth += pack('i', i)

