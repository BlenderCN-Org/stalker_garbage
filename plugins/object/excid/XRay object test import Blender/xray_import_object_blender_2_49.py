#                                           #
#    XRay Engine (S.T.A.L.K.E.R.) object    #
#       test import plugin for Blender      #
#                                           #
#          Anton 'excid' Gorenko            #
#              excid@mail.ru                #
#                                           #
#               (2007 June)                 #
#                                           #
 
from struct import *
import datetime
 
useBlender = True
try:
    from Blender import *
    from Blender.Mathutils import *
except:
    useBlender = False
 
 
f = open('C:\\test_import.object', 'rb')
s = f.read()
f.close()
 
 
def parseMeshData(s):
 
    p = 0
    print '\nunknown block =', hex(int(unpack('I', s[p : p + 4])[0]))
    p += 4
    size = unpack('I', s[p : p + 4])[0]
    print 'unknown block size =', size
    p += 4
    print 'unknown data =', map(hex, unpack('%dB' % (size,), s[p : p + size]))
    p += size
 
    print '\nname block =', hex(int(unpack('I', s[p : p + 4])[0]))
    p += 4
    nameSize = unpack('I', s[p : p + 4])[0]
    print 'name block size =', nameSize
    p += 4
    name = unpack('%ds' % (nameSize,), s[p : p + nameSize])[0][:-1]
    p += int(nameSize)
    print 'name =', name
 
    if useBlender:
        obj = Object.New('Mesh', name)
        mesh = Mesh.New(name)
        obj.link(mesh)
        scene = Scene.GetCurrent()
        scene.objects.link(obj)
 
    print '\nbbox block =', hex(int(unpack('I', s[p : p + 4])[0]))
    p += 4
    print 'bbox block size =', unpack('I', s[p : p + 4])[0]
    p += 4
    print 'bbox min = ', unpack('3f', s[p : p + 12])
    p += 12
    print 'bbox max = ', unpack('3f', s[p : p + 12])
    p += 12
 
    print '\nunknown block =', hex(int(unpack('I', s[p : p + 4])[0]))
    p += 4
    size = unpack('I', s[p : p + 4])[0]
    print 'unknown block size =', size
    p += 4
    print 'unknown data =', map(hex, unpack('%dB' % (size,), s[p : p + size]))
    p += size
 
    print '\nunknown block =', hex(int(unpack('I', s[p : p + 4])[0]))
    p += 4
    size = unpack('I', s[p : p + 4])[0]
    print 'unknown block size =', size
    p += 4
    print 'unknown data =', map(hex, unpack('%dB' % (size,), s[p : p + size]))
    p += size
 
    print '\nvertices block =', hex(int(unpack('I', s[p : p + 4])[0]))
    p += 4  
    print 'vertices block size =', unpack('I', s[p : p + 4])[0]
    p += 4  
    verticesCount = unpack('I', s[p : p + 4])[0]
    p += 4
    print 'vertices count =', verticesCount 
    for i in range(verticesCount):
        coords = unpack('3f', s[p : p + 12])
        print 'vertex%d =' % (i,), coords
        p += 12
 
        if useBlender:
            mesh.verts.extend([coords])
 
    print '\ntriangles block =', hex(int(unpack('I', s[p : p + 4])[0]))
    p += 4
    print 'triangles block size =', unpack('I', s[p : p + 4])[0]
    p += 4
 
    trianglesCount = unpack('I', s[p : p + 4])[0]
    p += 4
    print 'triangles count =', trianglesCount   
 
    faces = []
    for i in range(trianglesCount):
        vertices = unpack('6I', s[p : p + 24])
        print 'triangle%d =' % (i,), vertices
        p += 24
 
        faces.append(vertices)
 
    print '\nsmoothgroups block =', hex(int(unpack('I', s[p : p + 4])[0]))
    p += 4
    size = unpack('I', s[p : p + 4])[0]
    p += 4
    print 'smoothgroups block size =', size
    for i in range(size / 4):
        x = unpack('I', s[p : p + 4])[0]
        print 'triangle%d =' % (i,), hex(int(x))
        p += 4
 
    print '\nuv map block =', hex(int(unpack('I', s[p : p + 4])[0]))
    p += 4
    size = unpack('I', s[p : p + 4])[0]
    p += 4
    print 'uv map block size =', size
    count = unpack('I', s[p : p + 4])[0]
    p += 4
    print 'count =', count
 
    layerIndices = []
    uvIndices = []
    for i in range(count):
        unknown = unpack('5B', s[p : p + 5])
        p += 5
 
        uvIndex = int(unpack('I', s[p : p + 4])[0])
        p += 4
 
        print 'uv index =', map(hex, unknown), uvIndex
 
        layerIndices.append(unknown[1])
        uvIndices.append(uvIndex)
 
 
    print '\nmaterials block =', hex(int(unpack('I', s[p : p + 4])[0]))
    p += 4
    size = unpack('I', s[p : p + 4])[0]
    p += 4
    print 'materials block size =', size
    materialsCount = unpack('H', s[p : p + 2])[0]
    p += 2
    print 'materials count =', materialsCount
 
    for i in range(materialsCount):
        materialName = ''
        b = unpack('B', s[p : p + 1])[0]
        p += 1
        while b != 0:
            materialName = materialName + chr(b)
            b = unpack('B', s[p : p + 1])[0]
            p += 1
        print 'material%d name =' % (i,), materialName
 
        trianglesCount = unpack('I', s[p : p + 4])[0]
        p += 4
        print 'triangles count =', trianglesCount
 
        print 'triangles indices =', map(int, unpack('%dI' % (trianglesCount,), s[p : p + 4 * trianglesCount]))
        p += 4 * trianglesCount
 
    print '\ntexcoords block =', hex(int(unpack('I', s[p : p + 4])[0]))
    p += 4
    size = unpack('I', s[p : p + 4])[0]
    p += 4
    print 'texcoords block size =', size
    uvTablesCount = unpack('I', s[p : p + 4])[0]
    p += 4
    print 'uv tables count =', uvTablesCount
 
 
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
        print 'name =', chanelName
 
        x = unpack('B', s[p : p + 1])[0]
        p += 1
        print 'unknown =', x
        layerIndex = unpack('H', s[p : p + 2])[0]
        p += 2
        print 'layer index =', layerIndex   
        count = unpack('I', s[p : p + 4])[0]
        p += 4
        print 'uvs count =', count
 
        for j in range(count):
            uv = unpack('2f', s[p : p + 8])
            print 'uv%d =' % (j,), uv
            p += 8
 
            currentUv.append(uv)
        uvs.append(currentUv)
 
        for j in range(count):
            x = unpack('I', s[p : p + 4])[0]
            print 'index%d =' % (j,), int(x)
            p += 4
 
    i = 0
    while len(s) > p:
        x = unpack('I', s[p : p + 4])[0]
        print 'unknown index%d =' % (i,), int(x)
        p += 4  
        i += 1
 
    if useBlender:
        faceIndex = 0
        for faceInfo in faces:
            if faceInfo[4] == 0:
                faceInfo = faceInfo[2:] + faceInfo[:2]
            mesh.faces.extend(faceInfo[::2])
            face = mesh.faces[-1]
 
            faceUvs = []
            for i in faceInfo[1::2]:
                faceUvs.append(Vector(uvs[layerIndices[i]][uvIndices[i]]))
            face.uv = faceUvs
 
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
    print '\ngeometry\n'
    p = 0
    while p < len(s):
        i = unpack('I', s[p : p + 4])[0]    
        p += 4
        dataSize = unpack('I', s[p : p + 4])[0]
        print 'mesh%d data size = %d' % (i, dataSize)
        p += 4
        parseMeshData(s[p : p + dataSize])
        p += dataSize   
 
 
def parseMaterialBlock(s):
    print '\nmaterials\n'
    p = 0
    materialsCount = unpack('I', s[p : p + 4])[0]
    p += 4
    print 'materials count =', materialsCount
 
    for i in range(materialsCount):
        print '\n'
        materialName, p = parseString(s, p)
        print 'material%d name =' % (i,), materialName
 
        engineShader, p = parseString(s, p)
        print 'engine shader =', engineShader
 
        compilerShader, p = parseString(s, p)
        print 'compiler shader =', compilerShader
 
        gameMaterial, p = parseString(s, p)
        print 'game material =', gameMaterial   
 
        texturePath, p = parseString(s, p)
        print 'texture path =', texturePath
 
        texture, p = parseString(s, p)
        print 'texture =', texture
 
        print 'flags (2 sided, etc) =', hex(int(unpack('I', s[p : p + 4])[0]))
        p += 4  
 
        size = 8
        print 'unknown data =', map(hex, unpack('%dB' % (size,), s[p : p + size]))
        p += size   
 
 
def parseAuthorBlock(s):
    print '\nauthor\n'
    p = 0
    authorName, p = parseString(s, p)
    print 'author name =', authorName
 
    size = 4
    print 'creation date =', map(hex, unpack('%dB' % (size,), s[p : p + size]))
    p += size   
 
 
    modifierName, p = parseString(s, p)
    print 'modifier name =', modifierName
 
    print 'modification date =', map(hex, unpack('%dB' % (size,), s[p : p + size]))
    p += size   
 
 
def parseUserDataBlock(s):
    print '\nuser data\n'
    p = 0
    userData, p = parseString(s, p)
    print 'user data =', userData
 
 
def parseLODBlock(s):
    print '\nlod\n'
    p = 0
    reference, p = parseString(s, p)
    print 'lod reference =', reference  
 
 
def parseFlagsBlock(s):
    print '\nflags (model type)\n'
    p = 0
    flags = unpack('I', s[p : p + 4])[0]
    print 'model type =', hex(int(flags))
 
 
print '\n' * 3
 
p = 0
header = unpack('I', s[p : p + 4])[0]   
print 'header =', hex(int(header))
p += 4
 
dataSize = unpack('I', s[p : p + 4])[0] 
print 'data size =', dataSize
p += 4
 
while p < len(s):
    print '\n'
    print '=' * 79
    block = unpack('I', s[p : p + 4])[0]
    print 'block =', hex(int(block))
    p += 4
 
    blockSize = unpack('I', s[p : p + 4])[0]
    print 'block size =', blockSize
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
        print 'unknown data =', map(hex, unpack('%dB' % (blockSize,), s[p : p + blockSize]))
    p += blockSize