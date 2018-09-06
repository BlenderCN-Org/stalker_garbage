from struct import *
f = open(r'C:\1.object', 'rb')
s = f.read()
f.close()
import bpy
useBlender = True
def parseMeshData(s):
    #c = open(r'C:\1.txt', 'w')
    size = unpack('I', s[4:8])[0]
    p = 8
    p += size
    p += 4
    nameSize = unpack('I', s[p : p + 4])[0]
    p += 4
    name = unpack('%ds' % (nameSize,), s[p : p + nameSize])[0][:-1]
    p += int(nameSize)
    p += 36
    size = unpack('I', s[p : p + 4])[0]
    p += 4
    p += size
    p += 4
    size = unpack('I', s[p : p + 4])[0]
    p += 4
    p += size
    p += 8 
    verticesCount = unpack('I', s[p : p + 4])[0]
    p += 4
    abc = 0
    vert_coords = list(range(0,verticesCount,1))
    for i in range(verticesCount):
        coords = unpack('3f', s[p : p + 12])#Class tuple
        p += 12
        vert_coords[abc] = coords
        abc += 1
        #c.write(str(coords) + ', ')
    p += 8
    trianglesCount = unpack('I', s[p : p + 4])[0]
    p += 4
    faces = []#Class List
    for i in range(trianglesCount):
        vertices = unpack('6I', s[p : p + 24])
        p += 24
        faces.append(vertices[::2])
    #print(faces)
    p += 4
    size = unpack('I', s[p : p + 4])[0]
    p += 4
    m = int(size/4)
    for i in range(m):
        x = unpack('I', s[p : p + 4])[0]
        p += 4
    p += 4
    size = unpack('I', s[p : p + 4])[0]
    p += 4
    count = unpack('I', s[p : p + 4])[0]
    p += 4
    layerIndices = []
    uvIndices = []
    for i in range(count):
        unknown = unpack('5B', s[p : p + 5])
        p += 5
        uvIndex = int(unpack('I', s[p : p + 4])[0])
        p += 4
        layerIndices.append(unknown[1])
        uvIndices.append(uvIndex)
    p += 4
    size = unpack('I', s[p : p + 4])[0]
    p += 4
    materialsCount = unpack('H', s[p : p + 2])[0]
    p += 2
    for i in range(materialsCount):
        materialName = ''
        b = unpack('B', s[p : p + 1])[0]
        p += 1
        while b != 0:
            materialName = materialName + chr(b)
            b = unpack('B', s[p : p + 1])[0]
            p += 1
        trianglesCount = unpack('I', s[p : p + 4])[0]
        p += 4
        p += 4 * trianglesCount
    p += 4
    size = unpack('I', s[p : p + 4])[0]
    p += 4
    uvTablesCount = unpack('I', s[p : p + 4])[0]
    p += 4
    uvs = []#Class List
    for i in range(uvTablesCount):
        currentUv = []
        chanelName = ''
        b = unpack('B', s[p : p + 1])[0]
        p += 1
        while b != 0:
            chanelName = chanelName + chr(b)
            b = unpack('B', s[p : p + 1])[0]
            p += 1
        x = unpack('B', s[p : p + 1])[0]
        p += 1
        layerIndex = unpack('H', s[p : p + 2])[0]
        p += 2
        count = unpack('I', s[p : p + 4])[0]
        p += 4
        for j in range(count):
            uv = unpack('2f', s[p : p + 8])
            p += 8
            currentUv.append(uv)
        uvs.append(currentUv)
        for j in range(count):
            x = unpack('I', s[p : p + 4])[0]
            p += 4
    i = 0
    while len(s) > p:
        x = unpack('I', s[p : p + 4])[0]
        p += 4  
        i += 1
    if useBlender:
        mesh = bpy.data.meshes.new('mesh')
        object = bpy.data.objects.new('object', mesh)
        scene = bpy.context.scene
        scene.objects.link(object)
        mesh.from_pydata(vert_coords,(),faces)
        scene.update()
    
    
    
    #c.write(str(vert_coords) + '\n' + str(faces))
    #c.close()
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
        parseMeshData(s[p : p + dataSize])
        p += dataSize   
def parseMaterialBlock(s):
    p = 0
    materialsCount = unpack('I', s[p : p + 4])[0]
    p += 4
    for i in range(materialsCount):
        materialName, p = parseString(s, p)
        engineShader, p = parseString(s, p)
        compilerShader, p = parseString(s, p)
        gameMaterial, p = parseString(s, p)
        texturePath, p = parseString(s, p)
        texture, p = parseString(s, p)
        p += 4  
        size = 8
        p += size   
header = unpack('I', s[0:4])[0]
dataSize = unpack('I', s[4:8])[0] 
block = unpack('I', s[8:12])[0]
p=8
while p < len(s):
    block = unpack('I', s[p : p + 4 ])[0]
    p += 4
    blockSize = unpack('I', s[p : p + 4])[0]
    p += 4
    if block == 0x0910:
        parseGeometryBlock(s[p : p + blockSize])
    elif block == 0x0907:
        parseMaterialBlock(s[p : p + blockSize])       
    else:
        pass
    p += blockSize
print ('Finish')