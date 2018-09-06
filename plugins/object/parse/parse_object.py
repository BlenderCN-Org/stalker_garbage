# разбирает формат *.object (только статика)
# если запустить в Blender 2.67b, то импортируется меш без юви
# дата последних изменений - 29.04.2014

from struct import unpack
import time

start_time = time.time()

useBlender = True
try:
    import bpy
except:
    useBlender = False

f = open(r'c:\l01_escape_terrain.object', 'rb')
s = f.read()
f.close()

def parse_mesh_data(s):
    p = 0
    
    block_id = unpack('I', s[p : p + 4])[0]
    p += 4
    
    block_size = unpack('I', s[p : p + 4])[0]
    p += 4
    
    # print(hex(block_id), 'size =', block_size)
    
    mesh_version = unpack('h', s[p : p + 2])[0]
    p += 2
    # print('Mesh Version:', hex(mesh_version))
    
    block_id = unpack('I', s[p : p + 4])[0]
    p += 4
    
    block_size = unpack('I', s[p : p + 4])[0]
    p += 4
    
    # print(hex(block_id), 'size =', block_size)
    
    mesh_name = str(unpack('%ds' % block_size, s[p : p + block_size])[0])[2:-5]
    p += block_size
    # print('Mesh Name:', mesh_name)
    
    block_id = unpack('I', s[p : p + 4])[0]
    p += 4
    
    block_size = unpack('I', s[p : p + 4])[0]
    p += 4
    
    # print(hex(block_id), 'size =', block_size)
    
    bbox = unpack('6f', s[p : p + 24])
    p += 24
    # print('Bounding Box:\n', bbox[:3], '\n', bbox[3:])
    
    block_id = unpack('I', s[p : p + 4])[0]
    p += 4
    
    block_size = unpack('I', s[p : p + 4])[0]
    p += 4
    
    # print(hex(block_id), 'size =', block_size)
    
    flags = unpack('b', s[p : p + 1])[0]
    p += 1
    # print('Flags:', hex(flags))
    
    block_id = unpack('I', s[p : p + 4])[0]
    p += 4
    
    block_size = unpack('I', s[p : p + 4])[0]
    p += 4
    
    # print(hex(block_id), 'size =', block_size)
    
    options = unpack('8b', s[p : p + 8])
    p += 8
    # print('Options:', options)
    
    block_id = unpack('I', s[p : p + 4])[0]
    p += 4
    
    block_size = unpack('I', s[p : p + 4])[0]
    p += 4
    
    # print(hex(block_id), 'size =', block_size)
    
    vertex_count = unpack('I', s[p : p + 4])[0]
    p += 4
    # print('Vertex Count:', vertex_count)
    
    verts = []
    for i in range(vertex_count):
        coord_x = (unpack('f', s[p : p + 4]))[0]
        p += 4
        
        coord_y = (unpack('f', s[p : p + 4]))[0]
        p += 4
        
        coord_z = (unpack('f', s[p : p + 4]))[0]
        p += 4
        
        verts.append((coord_x, coord_z, coord_y))
    '''
    for i in verts:
        print(i)
    '''
    block_id = unpack('I', s[p : p + 4])[0]
    p += 4
    
    block_size = unpack('I', s[p : p + 4])[0]
    p += 4
    
    # print(hex(block_id), 'size =', block_size)
    
    face_count = unpack('I', s[p : p + 4])[0]
    p += 4
    # print('Face Count:', face_count)
    
    faces = []
    
    for i in range(face_count):
        vertices = unpack('6i', s[p : p + 24])
        p += 24
        
        faces.append(vertices[::2])
    
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
    
    '''
    for i in faces:
        print(i)
    '''
    block_id = unpack('I', s[p : p + 4])[0]
    p += 4
    
    block_size = unpack('I', s[p : p + 4])[0]
    p += 4
    
    # print(hex(block_id), 'size =', block_size)
    
    smooth_groups = []
    
    for i in range(int(block_size/4)):
        smooth_groups.append(unpack('i', s[p : p + 4])[0])
        p += 4
    '''
    for i in smooth_groups:
        print(i)
    '''
    block_id = unpack('I', s[p : p + 4])[0]
    p += 4
    
    block_size = unpack('I', s[p : p + 4])[0]
    p += 4
    
    # print(hex(block_id), 'size =', block_size)
    
    count = unpack('I', s[p : p + 4])[0]
    p += 4
    
    # print('Count', count)
    
    for i in range(count):
        set = unpack('b', s[p : p + 1])[0]
        p += 1
        
        vmap = unpack('i', s[p : p + 4])[0]
        p += 4
        
        vmap_entry = unpack('i', s[p : p + 4])[0]
        p += 4
        
        # print('vmref{0}: set{1}, vmap = {2}, vmap entry = {3}'.format(i, set, vmap, vmap_entry))
    
    block_id = unpack('I', s[p : p + 4])[0]
    p += 4
    
    block_size = unpack('I', s[p : p + 4])[0]
    p += 4
    
    # print(hex(block_id), 'size =', block_size)
    
    surface_count = unpack('h', s[p : p + 2])[0]
    p += 2
    # print('Surface Count =', surface_count)
    
    for i in range(surface_count):
        surface_name = ''
        ch = unpack('s', s[p : p + 1])[0]
        p += 1
        while ch != b'\x00':
            surface_name += str(ch)[2:-1]
            ch = unpack('s', s[p : p + 1])[0]
            p += 1
        # print('Surface Name:', surface_name)
        
        face_count = unpack('i', s[p : p + 4])[0]
        p += 4
        # print('Face Count in Surface:', face_count)
        
        for i in range(face_count):
            face_id = unpack('i', s[p : p + 4])[0]
            p += 4
            # print('face:', face_id)
    
    block_id = unpack('I', s[p : p + 4])[0]
    p += 4
    
    block_size = unpack('I', s[p : p + 4])[0]
    p += 4
    
    # print(hex(block_id), 'size =', block_size)
    
    uv_map_count = unpack('I', s[p : p + 4])[0]
    p += 4
    # print('UVs Count:', uv_map_count)
    
    for i in range(uv_map_count):
        uvmap_name = ''
        ch = unpack('s', s[p : p + 1])[0]
        p += 1
        while ch != b'\x00':
            uvmap_name += str(ch)[2:-1]
            ch = unpack('s', s[p : p + 1])[0]
            p += 1
        # print('\nUV Map Name:', uvmap_name)
        
        uvmap_entry_dimension = unpack('b', s[p : p + 1])[0]
        p += 1
        # print('UVmap Entry Dimension =', uvmap_entry_dimension)
        
        has_pidata = unpack('b', s[p : p + 1])[0]
        p += 1
        '''
        if has_pidata == 0:
            print('Has Discontig UV Map: No')
        elif has_pidata == 1:
            print('Has Discontig UV Map: Yes')
        else:
            print('Has Discontig UV Map: UNKNOW')
        '''
        vmap_type = unpack('b', s[p : p + 1])[0]
        p += 1
        
        '''
        if vmap_type == 0:
            print('VMap Type: UV')
        elif vmap_type == 1:
            print('VMap Type: Weight')
        else:
            print('VMap Type: UNKNOW')
        '''
        
        data_count = unpack('h', s[p : p + 2])[0]
        p += 2
        # print('Data Count = %i\n' % data_count)
        
        vertex = unpack('h', s[p : p + 2])[0]
        p += 2
        # print('Vertex =', vertex)
        
        
        for j in range(data_count):
            
            if uvmap_entry_dimension == 1 and vmap_type == 1:
                weight = unpack('f', s[p : p + 4])[0]
                p += 4
                # print('Weight =', weight)
            
            elif uvmap_entry_dimension == 2 and vmap_type == 0:
                uv_coord = unpack('2f', s[p : p + 8])
                p += 8
                # print('uv{0} = {1}'.format(j, uv_coord))
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
    
def parse_mesh(s):
    p = 0
    
    while p < len(s):
        mesh_id = unpack('I', s[p : p + 4])[0]
        p += 4
        
        mesh_data_size = unpack('I', s[p : p + 4])[0]
        p += 4
        # print('mesh%d data size = %d' % (mesh_id, mesh_data_size))
        
        parse_mesh_data(s[p : p + mesh_data_size])
        p += mesh_data_size

p = 0

block_id = unpack('i', s[p : p + 4])[0]
p += 4
# print(hex(block_id), end = ' ')

block_size = unpack('i', s[p : p + 4])[0]
p += 4
# print(block_size)

while p < len(s):
    block_id = unpack('i', s[p : p + 4])[0]
    p += 4
    # print(hex(block_id), end = ' ')
    
    block_size = unpack('i', s[p : p + 4])[0]
    p += 4
    # print(block_size)
    
    if block_id == 0x910:
        # взять срез из файла, чтобы меньше памяти занимало
        s = s[p : p + block_size]
        parse_mesh(s)
        break
    else:
        p += block_size

finish_time = time.time()
print('Time:', finish_time - start_time)

if useBlender == False:
    input()