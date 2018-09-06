# быстрый плагин (урезанный). импортирует только полигоны.
from struct import unpack
import time
start_time = time.time()
useBlender = True
try:
    import bpy
except:
    useBlender = False

f = open(r'c:\mp_atp_cuts.object', 'rb')
s = f.read()
f.close()

def parse_mesh_data(s):
    global FCount
    p = 14
    block_size = unpack('I', s[p : p + 4])[0]
    p += 4
    mesh_name = str(unpack('%ds' % block_size, s[p : p + block_size])[0])[2:-5]
    print(mesh_name)
    p += block_size
    p += 65
    vertex_count = unpack('I', s[p : p + 4])[0]
    p += 4
    verts = []
    for i in range(vertex_count):
        x, y, z = unpack('3f', s[p : p + 12])
        p += 12
        verts.append((x, z, y))
    p += 8
    face_count = unpack('I', s[p : p + 4])[0]
    FCount += face_count
    p += 4
    faces = []
    for i in range(face_count):
        v1 = unpack('i', s[p : p + 4])[0]
        p += 8
        v2 = unpack('i', s[p : p + 4])[0]
        p += 8
        v3 = unpack('i', s[p : p + 4])[0]
        p += 8
        faces.append((v1, v2, v3))
    
    if useBlender:
        mesh = bpy.data.meshes.new(mesh_name)
        object = bpy.data.objects.new(mesh_name, mesh)
        scene = bpy.context.scene
        scene.objects.link(object)
        mesh.from_pydata(verts,(),faces)
        bpy.context.scene.objects.active = object
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.flip_normals()
        bpy.ops.object.editmode_toggle()
        # Объединить в единый меш
        # bpy.ops.object.select_by_type(extend = False, type='MESH')
        # bpy.ops.object.join()


    
def parse_mesh(s):
    p = 0
    while p < len(s):
        p += 4
        mesh_data_size = unpack('I', s[p : p + 4])[0]
        p += 4
        parse_mesh_data(s[p : p + mesh_data_size])
        # Для больших файлов (LevelName_cuts.object)
        # if mesh_data_size > 100000:
        #     parse_mesh_data(s[p : p + mesh_data_size])
        p += mesh_data_size

p = 8
FCount = 0

while p < len(s):
    block_id = unpack('i', s[p : p + 4])[0]
    p += 4
    block_size = unpack('i', s[p : p + 4])[0]
    p += 4
    if block_id == 0x910:
        #s = s[p : p + block_size]
        parse_mesh(s[p : p + block_size])
        break
    else:
        p += block_size
finish_time = time.time()
print('Face Count =', FCount)
print('Time:', finish_time - start_time)
if useBlender == False:
    input()