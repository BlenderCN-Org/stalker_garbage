# разбирает формат *.object (только статика)
# если запустить в Blender 2.67b, то импортируется меш без юви
# дата последних изменений - 20.05.2014
# добавлены комментарии
# скопировал, чтобы попытаться сделать загрузку юви координат

path = r'c:\shadertest_teapot.object'  # загружаемый файл 3д модели

from struct import unpack       # для разбора двоичных данных
import time                     # использовал для контроля времени выполнения

start_time = time.time()        # время начала работы

useBlender = True
try:
    import bpy
    from mathutils import Vector
except:                 # если запущен не в блендере
    useBlender = False

f = open(path, 'rb')
s = f.read()
f.close()

def parse_mesh_data(s):
    block_id, block_size = unpack('2I', s[10 : 18])
    p = 18
    mesh_name = str(unpack('%ds' % block_size, s[p : p + block_size])[0])[2:-5]
    p += block_size + 57
    
    block_id, block_size, vertex_count = unpack('3I', s[p : p + 12]); p += 12
    verts = []
    
    for i in range(vertex_count):
        coord_x, coord_y, coord_z = (unpack('3f', s[p : p + 12])); p += 12
        verts.append((coord_x, coord_z, coord_y))

    block_id, block_size, face_count = unpack('3I', s[p : p + 12]); p += 12
    faces = []
    faces_uv = []
    
    for i in range(face_count):
        f1, f2, f3, f4, f5, f6 = unpack('6i', s[p : p + 24]); p += 24
        faces.append((f1, f3, f5)) # полигоны меша
        faces_uv.extend((f2, f4, f6)) # полигоны юви
    
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
        mesh.uv_textures.new()
    
    block_id, block_size = unpack('2I', s[p : p + 8]); p += 8
    smooth_groups = []
    
    for i in range(face_count):
        smooth_groups.append(unpack('i', s[p : p + 4])[0]); p += 4

    block_id, block_size, count = unpack('3I', s[p : p + 12]); p += 12
    layer_indices = []
    uv_indices = []
    
    for i in range(count):
        set = unpack('b', s[p : p + 1])[0]; p += 1
        vmap, vmap_entry = unpack('2i', s[p : p + 8]); p += 8
        
        layer_indices.append(set)
        uv_indices.append(vmap_entry)
        
    block_id, block_size, surface_count = unpack('iih', s[p : p + 10])
    p += 10
    
    for i in range(surface_count):
        surface_name = ''
        ch = unpack('b', s[p : p + 1])[0]
        p += 1
        while ch != 0:
            surface_name += chr(ch)
            ch = unpack('b', s[p : p + 1])[0]
            p += 1
        
        sface_count = unpack('i', s[p : p + 4])[0]; p += 4
        sface_ids = unpack('%di' % sface_count, s[p : p + (sface_count * 4)])
        p += sface_count * 4
    
    block_id, block_size, uv_map_count = unpack('3i', s[p : p + 12]); p += 12
    
    for i in range(uv_map_count):
        uvmap_name = ''
        ch = unpack('b', s[p : p + 1])[0]; p += 1
        while ch != 0:
            uvmap_name += chr(ch)
            ch = unpack('b', s[p : p + 1])[0]; p += 1
            
        uvmap_entry_dimension, has_pidata, vmap_type = unpack('3b', s[p : p + 3])
        p += 3
        
        data_count, vertex = unpack('2h', s[p : p + 4])
        p += 4
        
        verts_uv = []
        
        for j in range(data_count):
            
            if uvmap_entry_dimension == 1 and vmap_type == 1:
                weight = unpack('f', s[p : p + 4])[0]
                p += 4
                # print('Weight =', weight)
            
            elif uvmap_entry_dimension == 2 and vmap_type == 0:
                # Координаты юви вершин
                verts_uv.append(unpack('2f', s[p : p + 8])); p += 8
                '''if useBlender:
                    object.data.uv_layers.active.data[j].uv[0] = uv_x
                    object.data.uv_layers.active.data[j].uv[1] = uv_y'''
            else:
                break
                
        for j in range(data_count):
            index = unpack('i', s[p : p + 4])[0]
            p += 4
            # print('UV Index =', index)
            
        if has_pidata == 1:
            for j in range(data_count):
                face = unpack('i', s[p : p + 4])[0]
                p += 4
                # print('Face:', face)
    
    if useBlender:
        face_uv = []
        for i in faces_uv:
            face_uv.append(Vector(verts_uv[layer_indices[i]][uv_indices[i]])
        
        try:
            i = 0
            j = 0
            while True:
                object.data.uv_layers.active.data[i].uv[0] = face_uv[j]
                object.data.uv_layers.active.data[i].uv[1] = face_uv[j + 1]
                i += 1
                j += 2
        except:
            pass


def parse_mesh(s):
    # блок геометрии может иметь несколько мешей
    p = 0
    
    while p < len(s):
        mesh_id = unpack('I', s[p : p + 4])[0]  # порядковый номер меша
        p += 4
        
        mesh_data_size = unpack('I', s[p : p + 4])[0]   # размер данных одного меша
        p += 4
        # print('mesh%d data size = %d' % (mesh_id, mesh_data_size))
        
        parse_mesh_data(s[p : p + mesh_data_size])  # разобрать меш
        p += mesh_data_size

p = 0   # положение считывания из файла

block_id = unpack('i', s[p : p + 4])[0] # главный блок 0x7777
p += 4    # увеличить на 4, чтобы считать следующие байты
# print(hex(block_id), end = ' ')

block_size = unpack('i', s[p : p + 4])[0] # размер блока 0x7777
p += 4
# print(block_size)

while p < len(s):   # цикл для поиска блока, содержащего данные геометрии
    block_id = unpack('i', s[p : p + 4])[0]
    p += 4
    # print(hex(block_id), end = ' ')
    
    block_size = unpack('i', s[p : p + 4])[0]
    p += 4
    # print(block_size)
    
    if block_id == 0x910:   # блок геометрии
        # взять срез из файла, чтобы меньше памяти занимало
        s = s[p : p + block_size]
        parse_mesh(s)   # разобрать блок геометрии
        break   # остановить цикл, так как другие блоки искать уже не нужно
    else:
        p += block_size

finish_time = time.time()   # время окончания работы
# разница во времени между началом и окончанием работы
print('Time:', finish_time - start_time)

if useBlender == False:
    input()