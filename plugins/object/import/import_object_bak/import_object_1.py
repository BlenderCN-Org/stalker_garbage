# импортирует с юви (2.67)

from struct import *

useBlender = True
try:
    import bpy
    from mathutils import *
except:
    useBlender = False


f = open(r'c:\balon_01.object', 'rb')
s = f.read()
f.close()


def parseMeshData(s):
    
    p = 0
    p += 4
    size = unpack('I', s[p : p + 4])[0]
    p += 4
    p += size
    p += 4
    nameSize = unpack('I', s[p : p + 4])[0]
    p += 4
    name = unpack('%ds' % (nameSize,), s[p : p + nameSize])[0][:-1]
    p += int(nameSize)
    name = str(name)
    
    if useBlender:
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, mesh)
        scene = bpy.context.scene
        scene.objects.link(obj)
    
    p += 4
    p += 4
    p += 12
    p += 12
    p += 4
    size = unpack('I', s[p : p + 4])[0]
    p += 4
    p += size
    p += 4
    size = unpack('I', s[p : p + 4])[0]
    p += 4
    p += size
    p += 4  
    p += 4  
    verticesCount = unpack('I', s[p : p + 4])[0]
    p += 4
    verts = []
    for i in range(verticesCount):
        coords = unpack('3f', s[p : p + 12])
        p += 12
        verts.append((coords[0], coords[2], coords[1]))
    
    p += 4
    p += 4
    trianglesCount = unpack('I', s[p : p + 4])[0]
    p += 4
    
    faces = []
    faces_3d = []
    for i in range(trianglesCount):
        vertices = unpack('6I', s[p : p + 24])
        p += 24
        
        faces.append((vertices[0], vertices[1], vertices[4], vertices[5], vertices[2], vertices[3]))
        faces_3d.append((vertices[0], vertices[4], vertices[2]))
        
    p += 4
    size = unpack('I', s[p : p + 4])[0]
    p += 4
    for i in range(size // 4):
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
        mesh.from_pydata(verts,(),faces_3d)
        mesh.uv_textures.new()
        
        faceIndex = 0
        
        faceUvs = []
        
        for faceInfo in faces:
            if faceInfo[4] == 0:
                faceInfo = faceInfo[2:] + faceInfo[:2]

            
            for i in faceInfo[1::2]:
                faceUvs.append(Vector(uvs[layerIndices[i]][uvIndices[i]]))
        
        for n, i in enumerate(faceUvs):
            mesh.uv_layers[0].data[n].uv[0] = i[0]
            mesh.uv_layers[0].data[n].uv[1] = 1 - i[1]

            
    
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
    
    
def parseAuthorBlock(s):
    p = 0
    authorName, p = parseString(s, p)
    size = 4
    p += size   
    modifierName, p = parseString(s, p)
    p += size   
    
    
def parseUserDataBlock(s):
    p = 0
    userData, p = parseString(s, p)

    
def parseLODBlock(s):
    p = 0
    reference, p = parseString(s, p)
    

def parseFlagsBlock(s):
    p = 0
    flags = unpack('I', s[p : p + 4])[0]

p = 0
header = unpack('I', s[p : p + 4])[0]   
p += 4

dataSize = unpack('I', s[p : p + 4])[0] 
p += 4

while p < len(s):
    block = unpack('I', s[p : p + 4])[0]
    p += 4
    blockSize = unpack('I', s[p : p + 4])[0]
    p += 4  

    if block == 0x0910:
        parseGeometryBlock(s[p : p + blockSize])
    elif block == 0x0907:
        parseMaterialBlock(s[p : p + blockSize])
    elif block == 0x0922:
        parseAuthorBlock(s[p : p + blockSize])
    elif block == 0x0912:
        parseUserDataBlock(s[p : p + blockSize])
    elif block == 0x0925:
        parseLODBlock(s[p : p + blockSize])
    elif block == 0x0903:
        parseFlagsBlock(s[p : p + blockSize])       
    else:
        pass
    p += blockSize
