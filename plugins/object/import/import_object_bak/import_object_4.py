from time import time
start_time = time()
from struct import unpack

useBlender = True
try:
    import bpy
    from mathutils import Vector
except:
    useBlender = False


f = open(r'c:\1.object', 'rb')
s = f.read()
f.close()


def parseMeshData(s):

    p = 14
    nameSize = unpack('i', s[p : p + 4])[0]
    p += 4
    name = str(unpack('%ds' % nameSize, s[p : p + nameSize])[0])[2:-5]
    p += nameSize + 65
    verticesCount = unpack('i', s[p : p + 4])[0]
    p += 4
    verts = []
    for i in range(verticesCount):
        vx, vy, vz = unpack('3f', s[p : p + 12])
        p += 12
        verts.append((vx, vz, vy))
    
    p += 8
    trianglesCount = unpack('i', s[p : p + 4])[0]
    p += 4
    
    faces_all = []
    faces = []
    for i in range(trianglesCount):
        f1, tf1, f2, tf2, f3, tf3 = unpack('6i', s[p : p + 24])
        p += 24
        
        faces_all.append((f1, tf1, f3, tf3, f2, tf2))
        faces.append((f1, f3, f2))
        
    p += 4
    size = unpack('i', s[p : p + 4])[0]
    p += 4
    smooth_groups = unpack('%di' % (size//4), s[p : p + size])
    p += size + 8
    
    count = unpack('i', s[p : p + 4])[0]
    p += 4
    
    layerIndices = []
    uvIndices = []
    for i in range(count):
        set = unpack('b', s[p : p + 1])[0]
        p += 1
        
        vmap = unpack('i', s[p : p + 4])[0]
        p += 4
        
        uvIndex = unpack('i', s[p : p + 4])[0]
        p += 4
        
        layerIndices.append(set)
        uvIndices.append(uvIndex)
    
    
    p += 8
    materialsCount = unpack('h', s[p : p + 2])[0]
    p += 2
    
    material_names = []
    triangles_indices = []
    
    for i in range(materialsCount):
        materialName = ''
        b = unpack('b', s[p : p + 1])[0]
        p += 1
        while b != 0:
            materialName = materialName + chr(b)
            b = unpack('b', s[p : p + 1])[0]
            p += 1
        
        material_names.append(materialName)

        trianglesCount = unpack('I', s[p : p + 4])[0]
        p += 4

        triangles_indices.append(unpack('%di' % (trianglesCount), s[p : p + 4 * trianglesCount]))
        p += 4 * trianglesCount
        
    p += 8
    uvTablesCount = unpack('I', s[p : p + 4])[0]
    p += 4
    
    uvs = []
    for i in range(uvTablesCount):
        currentUv = []
        chanelName = ''
        b = unpack('B', s[p : p + 1])[0]
        p += 1
        while b != 0:
            chanelName = chanelName + chr(b)
            b = unpack('B', s[p : p + 1])[0]
            p += 1
        
        uvmap_entry_dimension = unpack('b', s[p : p + 1])[0]
        p += 1
        has_pidata = unpack('b', s[p : p + 1])[0]
        p += 1
        vmap_type = unpack('b', s[p : p + 1])[0]
        p += 1
        
        count = unpack('h', s[p : p + 2])[0]
        p += 2
        
        vertex = unpack('h', s[p : p + 2])[0]
        p += 2
        
        for j in range(count):
            if uvmap_entry_dimension == 1 and vmap_type == 1:
                weight = unpack('f', s[p : p + 4])[0]
                p += 4
                # print('Weight =', weight)
                
            elif uvmap_entry_dimension == 2 and vmap_type == 0:
                uv = unpack('2f', s[p : p + 8])
                p += 8
                # print('uv{0} = {1}'.format(j, uv_coord))
                currentUv.append(uv)
        
        if uvmap_entry_dimension == 2 and vmap_type == 0:
            uvs.append(currentUv)
        
        
        for j in range(count):
            index = unpack('i', s[p : p + 4])[0]
            p += 4
            # print('UV Index =', index)
            
        if has_pidata == 1:
            for j in range(count):
                face = unpack('i', s[p : p + 4])[0]
                p += 4
                # print('Face:', face)
    
    if useBlender:
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, mesh)
        scene = bpy.context.scene
        scene.objects.link(obj)
        mesh.from_pydata(verts, (), faces)
        for n, mat_name in enumerate(material_names):
            material = bpy.data.materials.new(mat_name)
            bpy.context.scene.objects.active = obj
            bpy.ops.object.material_slot_add()
            obj.material_slots[n].material = material
        
        for n, indices in enumerate(triangles_indices):
            for i in indices:
                mesh.polygons[i].material_index = n
        
        mesh.uv_textures.new()
        faceUvs = []
        
        for faceInfo in faces_all:
            if faceInfo[4] == 0:
                faceInfo = faceInfo[2:] + faceInfo[:2]

            
            for i in faceInfo[1::2]:
                faceUvs.append(Vector(uvs[layerIndices[i]][uvIndices[i]]))
        
        for n, i in enumerate(faceUvs):
            mesh.uv_layers[0].data[n].uv[0] = i[0]
            mesh.uv_layers[0].data[n].uv[1] = 1 - i[1]
    
    return material_names

            
    
def parseString(s, p):
    string = ''
    b = unpack('B', s[p : p + 1])[0]
    p += 1
    while b != 0:
        string = string + chr(b)
        b = unpack('B', s[p : p + 1])[0]
        p += 1
    return string, p
    

    
def parseGeometryBlock(s):
    p = 0
    while p < len(s):
        i = unpack('I', s[p : p + 4])[0]    
        p += 4
        dataSize = unpack('I', s[p : p + 4])[0]
        p += 4
        material_names = parseMeshData(s[p : p + dataSize])
        p += dataSize   
    return material_names

def parseMaterialBlock(s, material_names):
    p = 0
    materialsCount = unpack('I', s[p : p + 4])[0]
    p += 4

    textures = []
    
    for i in range(materialsCount):
        materialName, p = parseString(s, p)
        engineShader, p = parseString(s, p)
        compilerShader, p = parseString(s, p)
        gameMaterial, p = parseString(s, p)
        texturePath, p = parseString(s, p)
        texture, p = parseString(s, p)
        
        path = 'T:\\' + texturePath + '.dds'
        try:
            image = bpy.data.images.load(path)
        except:
            print("Cannot load image %s" % path)
        
        texture = bpy.data.textures.new(materialName, type = 'IMAGE')
        texture.image = image
        textures.append(texture)
        p += 12
    
    for n, name in enumerate(material_names):
        tex_slot = bpy.data.objects[-1].material_slots[name].material.texture_slots.add()
        tex_slot.texture = textures[n]
    
    mesh = bpy.data.objects[-1].data
    n = 0
    for i in mesh.polygons:
        mat = i.material_index
        image = bpy.data.objects[-1].material_slots[mat].material.texture_slots[0].texture.image
        bpy.data.objects[-1].data.uv_textures[0].data[n].image = image
        n += 1
         

p = 8    # 0x7777

while p < len(s):
    block, blockSize = unpack('2i', s[p : p + 8])
    p += 8 

    if block == 0x0910:
        material_names = parseGeometryBlock(s[p : p + blockSize])
    elif block == 0x0907:
        parseMaterialBlock(s[p : p + blockSize], material_names)
    p += blockSize

finish_time = time()
print(finish_time - start_time, 'sec')

if not useBlender:
    input('OK')