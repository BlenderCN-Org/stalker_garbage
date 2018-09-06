#                                           #
#    XRay Engine (S.T.A.L.K.E.R.) object    #
#        export plugin for Blender          #
#                                           #
#          Anton 'excid' Gorenko            #
#              excid@mail.ru                #
#                                           #
#               (2007 June)                 #
#                                           #

if 0:
    materialsPath = 'x:\\rawdata\\textures\\'
    exportPath = 'x:\\import\\xrayexport\\'
    materialsInfoFile = 'x:\\import\\xrayexport\\materials.txt'
else:
    materialsPath = '/home/excid/.wine/drive_c/X-Ray SDK/level_editor/rawdata/textures/'
    exportPath = '/home/excid/.wine/drive_c/X-Ray SDK/level_editor/import/xrayexport/'
    materialsInfoFile = '/home/excid/.wine/drive_c/X-Ray SDK/level_editor/import/xrayexport/materials.txt'

# try:
    # import psyco
    # psyco.profile()
    # print '(with psyco)'
# except ImportError:
    # pass

from struct import *
import copy
from time import time

from Blender import *


def normalizeName(s):
    return filter(lambda x: x.isalnum() or x == '_', s.lower())
    

def packString(s):
    l = len(s) + 1
    return pack(str(l) + 's', s)

    
def packStringWithLen(s):
    l = len(s) + 1
    return pack('I' + str(l) + 's', l, s)

    
def packGeometryData():
    geometryData = ''
                
    for index, obj in enumerate(objects):   
        name = normalizeName(obj.name)
        print '  exporting mesh %d %s (%s)' % (index, name, obj.name)
        
        for o in scene.objects:
            o.sel = False
        obj.sel = True
        Object.Duplicate(mesh = 0)          
        
        dupliObj = Object.GetSelected()[0]
        mesh = Mesh.New()
        b = True
        while b:
            b = False
            for modifier in dupliObj.modifiers:
                if modifier.type == Modifier.Types.EDGESPLIT:
                    dupliObj.modifiers.remove(modifier)
                    b = True
                    break
        mesh.getFromObject(dupliObj.name)           
        dupliObj.link(mesh)         
        
        obj = Object.New('Mesh', 'temp')
        mesh = Mesh.New()
        obj.link(mesh)
        scene.objects.link(obj)
        obj.join([dupliObj])
                
        mesh = obj.getData(False, True)
        mesh.sel = True
        mesh.quadToTriangle()
        
        Redraw() # hack: for bbox recalculating (http://www.blender.org/forum/viewtopic.php?t=11574)
        
        scene.objects.unlink(obj)
        scene.objects.unlink(dupliObj)
        group.objects.unlink(dupliObj)
                
        data = ''
                
        data += pack('2I2B', 0x1000, 2, 0x11, 0x0) # unknown data
        data += pack('I', 0x1001) + packStringWithLen(name)
        
        data += pack('2I', 0x1004, 24) 
        box = obj.getBoundBox()
        #data += pack('3f', *box[0]) +  pack('3f', *box[-2])
        data += pack('3f', -1000.0, -1000.0, -1000.0) + pack('3f', 1000.0, 1000.0, 1000.0)
        
        data += pack('2IB', 0x1002, 1, 0x5) # unknown data
        data += pack('2I8B', 0x1010, 8, *[0x0] * 8) # unknown data
        
        #print '  ', 4, time() - startTime
        vertsCount = len(mesh.verts)
        data += pack('3I', 0x1005, vertsCount * 12 + 4, vertsCount) + \
                ''.join([pack('3f', vert.co[0], vert.co[2], vert.co[1]) for vert in mesh.verts])
        
        if not mesh.faceUV:
            raise '    error: mesh has not uvs'
        
        def isFaceValid(face):
            a = face.verts[0].co - face.verts[1].co
            b = face.verts[2].co - face.verts[1].co
            s = 0.5 * (Mathutils.CrossVecs(a, b)).length
            return s > 0.00001
        
        #print '  ', 5, time() - startTime
        faces = []
        for face in mesh.faces:            
            face.sel = True
            faces.append(face)
            if not (len(face.verts) == 3 and isFaceValid(face)):
                print '    invalid face\n     ', '\n      '.join([str(v.co) for v in face.verts])
                Window.SetCursorPos(face.verts[0].co)
        #print '  ', 6, time() - startTime
        uvTable = {}
        uvMap = []
        uvs = []
        for face in faces:
            for uv in face.uv:
                uv = tuple(uv)
                try:
                    uvMap.append(uvTable[uv])
                except:
                    uvs.append(uv)
                    l = len(uvs) - 1
                    uvMap.append(l)
                    uvTable[uv] = l
                
        #print '  ', 7, time() - startTime
        
        facesCount = len(faces)
        data += pack('3I', 0x1006, facesCount * 6 * 4 + 4, facesCount) + \
                ''.join([pack('6I', f.v[0].index, f.index * 3 + 0, \
                                    f.v[2].index, f.index * 3 + 2, \
                                    f.v[1].index, f.index * 3 + 1) for f in faces if isFaceValid(face)])         
        #print '  ', 8, time() - startTime
        
        # smoothgroups
        smoothGroups = [set() for f in faces]
            
        edgesSharpness = dict([(e.key, e.flag & Mesh.EdgeFlags.SHARP) for e in mesh.edges])
        #print '  ', 80, time() - startTime
        edgeFaces = dict([(e.key, []) for e in mesh.edges])
        #print '  ', 80, time() - startTime
        for face in mesh.faces:
            for key in face.edge_keys:
                edgeFaces[key].append(face)
        
        facesGroups = [-1 for f in faces]
        #print '  ', 81, time() - startTime
        
        def getChildren(face):
            children = []
            for key in face.edge_keys:
                if not edgesSharpness[key]:
                    for f in edgeFaces[key]:
                        if (f is not face) and (facesGroups[f.index] == -1):
                            children.append(f)
            return children
                            
        def fillGroup(face, groupIndex):
            faces = (face,)
            while faces:                
                for face in faces:
                    facesGroups[face.index] = groupIndex
                newFaces = set()
                for face in faces:
                    newFaces.update(getChildren(face))
                faces = tuple(newFaces)
                
        nothingUsed = False
        groupCount = 0
        for face in faces:
            if facesGroups[face.index] == -1:             
                fillGroup(face, groupCount)
                groupCount += 1
        #print groupCount
        #print '  ', 82, time() - startTime
        def getNeiborGroups(face):
            groups = set()
            for key in face.edge_keys:
                if edgesSharpness[key]:
                    groups = reduce(lambda x, y: x.union(y), [[facesGroups[f.index]] for f in edgeFaces[key] if f is not face], groups)                  
                    for f in edgeFaces[key]:
                        if f is not face:
                            groups.union(smoothGroups[f.index]) 
            groups.discard(facesGroups[face.index])
            return groups
            
        neiborGroups = [set() for i in range(groupCount)]
        for face in faces:
            faceGroup = facesGroups[face.index]
            neiborGroups[faceGroup] = neiborGroups[faceGroup].union(getNeiborGroups(face))
        
        #print neiborGroups
        neiborGroups = map(lambda x: tuple(x), neiborGroups)
        smoothGroups = [-1 for i in range(groupCount)]
        
        #print '  ', 83, time() - startTime
        
        def getNeiborSGroups(group):
            smGroups = set()
            for neiborGroup in neiborGroups[group]:
                smGroups.add(smoothGroups[neiborGroup])
            smGroups.discard(-1)
            return tuple(smGroups)
            
        def fillSGroup(group):
            nSGroups = getNeiborSGroups(group)
            nGroups = neiborGroups[group]
            for i in set(range(32)).difference(nSGroups):
                smoothGroups[group] = i
                b = True
                usedNeibors = []
                for neibor in nGroups:
                    if smoothGroups[neibor] == -1:
                        usedNeibors.append(neibor)
                        if not fillSGroup(neibor):
                            b = False
                            break
                if not b:
                    for neibor in usedNeibors:
                        smoothGroups[neibor] = -1
                else:
                    return True
            if not b:
                smoothGroups[group] = -1
                return False
        
        fillSGroup(1)
        #print smoothGroups
        #print '  ', 84, time() - startTime
        data += pack('2I', 0x1013, facesCount * 4) + \
                ''.join([pack('I', smoothGroups[facesGroups[f.index]] + 1) for f in faces])
        #print '  ', 9, time() - startTime
        
        # uv map
        data += pack('3I', 0x1008, facesCount * 3 * 9 + 4, facesCount * 3) + \
                ''.join([pack('B', 0x1) + pack('2I', 0x0, uv) for uv in uvMap])
        #print '  ', 10, time() - startTime
        
        # materials
        global materials
        materials = {}
        _materials = {}
        for i, f in enumerate(faces):
            try:
                _materials[f.image.filename].add(i)
            except:
                _materials[f.image.filename] = set([i])
        for key, value in _materials.iteritems():
            #print key
            #print key.split(materialsPath)[1].split('.')[0]
            materials['test'] = value
#materials[key.split(materialsPath)[1].split('.')[0]] = value
        
        matData = ''
        matCount = len(materials)
        for matName in materials.keys():
            matInfo = materials[matName]
            matData += packString(matName) + pack('I', len(matInfo)) + \
                       ''.join([pack('I', f) for f in matInfo])     
        data += pack('2IH', 0x1009, len(matData) + 2, matCount) + matData
        #print '  ', 11, time() - startTime  
        
        # uv
        layersCount = 2
        uvData = pack('I', layersCount)
        layer = 0
        uvData += packString('Texture') + pack('3B', layersCount, layer, 0x0)
        uvData += pack('I', len(uvs)) + \
                  ''.join([pack('2f', uv[0], uv[1]) for uv in uvs]) + \
                  ''.join([pack('I', 0x0) for i in range(len(uvs))])
        layer = 1
        uvData += packString('Texture') + pack('3B', layersCount, layer, 0x0)
        uvData += pack('I', 0)
        #uvData += ''.join([pack('I', 0x0) for i in range(len(uvs))])
        data += pack('2I', 0x1012, len(uvData)) + uvData
        
        data = pack('2I', index, len(data)) + data
        #print '  ', 12, time() - startTime
        print '  done\n'
        
        geometryData += data
        
    return geometryData

    
def packMaterialsData():
    matsCount = len(materials)
    matData = pack('I', matsCount)
    for matName in materials.keys():
        matData += packString(matName) 
        if materialsInfo.has_key(matName):
            matInfo = materialsInfo[matName]
            matData += packString(matInfo[0]) + packString(matInfo[1]) + packString(matInfo[2])
            flags = matInfo[3]
        else:
            matData += packString('default') + packString('default') + packString('default')
            flags = 0
        
        matData += packString(matName) + packString('Texture')
        matData += pack('I', flags)
        matData += pack('8B', 0x12, 0x1, 0x0, 0x0, 0x1, 0x0, 0x0, 0x0) # unknown data
    
    return matData
    
    
def packAuthorData():
    author = 'excid'
    authorData = packString(author) + pack('I', 0x0) + \
                 packString(author) + pack('I', 0x0)
    return authorData

    
def loadMaterials():
    materials = {}
    
    f = open(materialsInfoFile, 'r')

    for s in f.readlines():
        print s
        parts = s.split('|')
        if parts[0].startswith('#') or len(parts) < 5:
            continue
        materials[parts[0]] = parts[1], parts[2], parts[3], int(parts[4])
    return materials
    

print '\n' * 2 + '*' * 80,
print '\n'.join(map(lambda s: s.center(78),
    ['XRay Engine (S.T.A.L.K.E.R.) object',
     'export plugin for Blender',
     '',
     'Anton \'excid\' Gorenko',
     'excid@mail.ru',
     '',
     '(2007 June)']))
print '*' * 80 + '\n'

materialsInfo = loadMaterials()
materials = {}

startTime = time()

Window.EditMode(0)
scene = Scene.GetCurrent()

groups = Group.Get()
for group in groups:
    
    name = normalizeName(group.name)
    print 'exporting group %s(%s)' % (name, group.name)
    
    objects = [obj for obj in group.objects if obj.getType() == 'Mesh']
    if not objects:
        print 'done'
        
    data = ''

    # version
    data += pack('IIH', 0x0900, 2, 0x10)

    # user data
    userData = ''
    data += pack('I', 0x0912) + packStringWithLen(userData)

    # lod reference
    lodReference = ''
    data += pack('I', 0x0925) + packStringWithLen(lodReference)

    # flags
    flags = 0x0
    data += pack('3I', 0x0903, 4, flags)

    # geometry data
    geometryData = packGeometryData()
    data += pack('II', 0x0910, len(geometryData)) + geometryData

    # materials data
    materialsData = packMaterialsData()
    data += pack('II', 0x0907, len(materialsData)) + materialsData

    # author data
    authorData = packAuthorData()
    data += pack('II', 0x0922, len(authorData)) + authorData
    
    f = open('%s%s.object' % (exportPath, name, ), 'wb')

    f.write(pack('I', 0x7777))
    f.write(pack('I', len(data)))
    f.write(data)

    f.close()
    
    print 'done\n'

finishTime = time()
print '\ntime %.2f' % (finishTime - startTime,)