from struct import unpack
import time

start_time = time.time()

try:
    import bpy
    use_blender = True
except:
    use_blender = False

f = open(r'c:\level.cform', 'rb')
s = f.read()
f.close()

p = 0
version = unpack('i', s[p : p + 4])[0]
p += 4
# print('Version:', version)

vertex_count = unpack('i', s[p : p + 4])[0]
p += 4
print('Vertex Count:', vertex_count)

face_count = unpack('i', s[p : p + 4])[0]
p += 4
print('Face Count:', face_count)

bbox_diagonal = unpack('6f', s[p : p + 24])
p += 24
# print('Bbox Diagonal:', bbox_diagonal[:3], bbox_diagonal[3:], sep = '\n\t')

verts = []

for i in range(vertex_count):
    vx, vy, vz = unpack('3f', s[p : p + 12])
    p += 12
    verts.append((vx, vz, vy))
    # print('Vertex%d:' % (i), vertex_coord)

faces = []

for i in range(face_count):
    f1, f2, f3 = unpack('3i', s[p : p + 12])
    p += 12
    # print('\nFace%d' % i, face_index)
    
    faces.append((f1, f3, f2))
    
    material_id = unpack('b', s[p : p + 1])[0]
    p += 1
    # print('Material ID:', material_id)
    
    flags = unpack('b', s[p : p + 1])[0]
    p += 1
    # print('Flags:', flags)
    
    sector_id = unpack('h', s[p : p + 2])[0]
    p += 2
    # print('Sector:', sector_id)
    
if use_blender:
    mesh = bpy.data.meshes.new('level_cform')
    object = bpy.data.objects.new('level_cform', mesh)
    scene = bpy.context.scene
    scene.objects.link(object)
    mesh.from_pydata(verts, (), faces)
    finish_time = time.time()
    print('FINISH: {}\n'.format(finish_time - start_time))

if not use_blender:
    input('OK')