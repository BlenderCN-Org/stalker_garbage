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
from time import time
useBlender = True
try:
	import bpy
	import mathutils
except:
    useBlender = False

def un_i(s, p):	# Unpack Integer
	return unpack('I', s[p : p + 4])[0]

def un_s(s, p):		# Unpack String
	return unpack('B', s[p : p + 1])[0]

def parse_string(s, p):
	string = ''
	b = 1	# Стартовое значение b (может быть любым кроме 0, чтобы условие входа в цикл было True)
	while b != 0:
		b = un_s(s, p)
		string += chr(b)
		p += 1
	return string, p

def parseMeshData(s):
    p = 4
    while p < len(s):
        data_size = un_i(s, p)
        p += 4
        s = s[p : p + data_size]
        p += data_size
    p = 4
    size = un_i(s, p)
    p += size + 8
    nameSize = un_i(s, p)
    p += 4
    name = unpack('%ds' % (nameSize,), s[p : p + nameSize])[0][:-1]
    p += int(nameSize) + 36
    size = unpack('I', s[p : p + 4])[0]
    p += size +8
    size = unpack('I', s[p : p + 4])[0]
    p += size + 12
    verticesCount = unpack('I', s[p : p + 4])[0]
    p += 4
    abc = 0
    vert_coords = list(range(0,verticesCount,1))
    for i in range(verticesCount):
        coords = unpack('3f', s[p : p + 12])
        x = coords[0]
        y = coords[1]
        z = coords[2]
        p += 12
        vert_coords[abc] = (x, z, y)
        abc += 1
    p += 8
    trianglesCount = unpack('I', s[p : p + 4])[0]
    p += 4
    faces = []
    faces_all = []
    for i in range(trianglesCount):
        vertices = unpack('6I', s[p : p + 24])
        p += 24
        faces_all.append(vertices)
        faces.append(vertices[::2])
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
        b = un_s(s, p)
        p += 1
        while b != 0:
            materialName = materialName + chr(b)
            b = un_s(s, p)
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
        b = un_s(s, p)
        p += 1
        while b != 0:
            chanelName = chanelName + chr(b)
            b = un_s(s, p)
            p += 1
        x = un_s(s, p)
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
        mesh = bpy.data.meshes.new('mesh')				# Создаём меш
        object = bpy.data.objects.new('object', mesh)	# Создаём объект
        scene = bpy.context.scene						# Активная сцена
        scene.objects.link(object)						# Присоединяем созданный объект активной сцене
        mesh.from_pydata(vert_coords,(),faces)			# Присваиваем вершины и полигоны мешу
        bpy.context.scene.objects.active = object		# Объект делается активным
        bpy.ops.object.editmode_toggle()				# Заходим в режим редактирования
        bpy.ops.mesh.flip_normals()						# Инвертируем нормали
        bpy.ops.object.editmode_toggle()				# Выходим из режима редактирования
        mesh.uv_textures.new()


        for faceInfo in faces_all:
            if faceInfo[4] == 0:
                faceInfo = faceInfo[2:] + faceInfo[:2]
            #mesh.faces.extend(faceInfo[::2])
            #face = mesh.faces[-1]

            faceUvs = []
            for i in faceInfo[1::2]:
                vert_uv = mathutils.Vector(uvs[layerIndices[i]][uvIndices[i]])
                object.data.uv_layers.active.data[i].uv[0] = vert_uv[0]
                object.data.uv_layers.active.data[i].uv[1] = 1 - vert_uv[1]
            #face.uv = faceUvs




"""
        for i in range(verticesCount):
            object.data.uv_layers.active.data[i].uv[0] = uvs[0][i][0]
            object.data.uv_layers.active.data[i].uv[1] = uvs[0][i][1]
        scene.update()
"""

def EOBJ_CHUNK_MESHES(s):		# Geometry Block
	p = 4
	while p < len(s):
		data_size = un_i(s, p)
		p += 4
		s = s[p : p + data_size]
		p += data_size   

def EOBJ_CHUNK_SURFACES_2(s):		# Material Block
	p = 0
	materialsCount = unpack('I', s[p : p + 4])[0]
	p += 4
	for i in range(materialsCount):
		materialName, p = parse_string(s, p)
		engineShader, p = parse_string(s, p)
		compilerShader, p = parse_string(s, p)
		gameMaterial, p = parse_string(s, p)
		texturePath, p = parse_string(s, p)
		texture, p = parse_string(s, p)
		p += 4  
		size = 8
		p += size

def parse_object(s):
	start_time = time()
	p = 0
	header = un_i(s, p)
	p += 4
	data_size = un_i(s, p)
	p += 4
	while p < len(s):
		block = un_i(s, p)
		p += 4
		block_size = un_i(s, p)
		p += 4  
		sb = s[p : p + block_size]	# часть файла, которая содержит один блок с размером block_size.
		if block == 0x0907:
			EOBJ_CHUNK_SURFACES_2(sb)
		elif block == 0x0910:
			parseMeshData(sb)
		else:
			pass
		p += block_size
	finish_time = time()
	print('Time: ', (finish_time - start_time), '\n')
	del p, sb, block_size, block, data_size, header


path = 'c:\\'
files = ('1.object', '2.object', '3.object')

for i in files:
	print(i)
	f = open(path + i, 'rb')
	s = f.read()
	f.close()
	parse_object(s)
	del s