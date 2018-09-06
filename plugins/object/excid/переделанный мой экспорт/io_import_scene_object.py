#                                           #
#    XRay Engine (S.T.A.L.K.E.R.) object    #
#       test import plugin for Blender      #
#                                           #
#          Anton 'excid' Gorenko            #
#              excid@mail.ru                #
#                                           #
#               (2007 June)                 #
#                                           #

#     Адаптировал для 2.67 - Pavel_Blend
#     Дата последних изменений 15.06.2014

#     Исправил старые баги, добавил новые - Denis Mikhaylov
#     Дата последних изменений 01.11.2014


bl_info = {
	"name": "Import XRay Engine (S.T.A.L.K.E.R.) Objects",
	"author": "excid & Pavel_Blend & Denis Mikhaylov",
	"version": (1, 0),
	"blender": (2, 70, 0),
	"location": "File > Import > XRay Engine Object (.object)",
	"description": "Imports a .object file.",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Import"}


from struct import unpack

import os

import bpy
from mathutils import Vector

is_debug = False #Импортировать в отладочном режиме
textures_path = 'D:\\Program Files\\X-Ray SDK\\editors\\gamedata\\textures\\' #Путь к текстурам
debug_file_name = "C:\\blenger_plug.log"
debug_file = open(debug_file_name, 'w')

#Вывести отладочное сообщение
def debug(s):
	if is_debug:
		try:
			debug_file.write(str(s))
			debug_file.write('\n')
			debug_file.flush()
		except:
			pass


#Получить число с плавающей точкой
def parseFloat(s, p, count = 1):
	size = 4 * count
	value = unpack('%df' % (count), s[p : p + size])
	
	p += size
	
	if count == 1:
		return value[0], p
	else:
		return value, p

#Получить целое 32-х разрядное число
def parseInteger(s, p, count = 1):
	size = 4 * count
	value = unpack('%di' % (count), s[p : p + size])
	
	p += size
	
	if count == 1:
		return value[0], p
	else:
		return value, p

#Получить целое 16-ти разрядное число
def parseShort(s, p, count = 1):
	size = 2 * count
	value = unpack('%dh' % (count), s[p : p + size])
	
	p += size
	
	if count == 1:
		return value[0], p
	else:
		return value, p

#Получить целое 8-ми разрядное число
def parseByte(s, p, count = 1):
	size = 1 * count
	value = unpack('%db' % (count), s[p : p + size])
	
	p += size
	
	if count == 1:
		return value[0], p
	else:
		return value, p

#Получить строку
def parseString(s, p):
	string = ''
	b, p = parseByte(s, p)
	while b != 0:
		string += chr(b)
		b, p = parseByte(s, p)
	return string, p

#Получить один мешь-объект
def parseMeshData(s):

	p = 14 #Попускаем неизвестные данные
	
	nameSize, p = parseInteger(s, p) #Длинна названия подобъекта
	
	#Название подобъекта
	name = str(unpack('%ds' % nameSize, s[p : p + nameSize])[0])[2:-5]
	p += nameSize + 65
	
	verticesCount, p = parseInteger(s, p) #Количество вертексов
	verts = [] #Вертексы
	for i in range(verticesCount):
		vx, p = parseFloat(s, p)
		vy, p = parseFloat(s, p)
		vz, p = parseFloat(s, p)
		verts.append(((vx, vz, vy)))
	
	p += 8
	
	trianglesCount, p = parseInteger(s, p) #Количество треугольников
	
	faces_all = [] #Треугольники + текстурная координата
	faces = [] #Треугольники
	for i in range(trianglesCount):
		f1, p = parseInteger(s, p)
		tf1, p = parseInteger(s, p)
		f2, p = parseInteger(s, p)
		tf2, p = parseInteger(s, p)
		f3, p = parseInteger(s, p)
		tf3, p = parseInteger(s, p)
        
		faces_all.append((f1, tf1, f3, tf3, f2, tf2))
		faces.append((f1, f3, f2))
		
	p += 4
	size, p = parseInteger(s, p) #Количество групп сглаживания
	
	smooth_groups = unpack('%di' % (size//4), s[p : p + size]) #Группы сглаживания
	p += size + 8
	
	count, p = parseInteger(s, p) #Количество текстурных координат
	
	layerIndices = []
	uvIndices = []
	for i in range(count):
		set, p = parseByte(s, p)
		
		vmap = unpack('4b', s[p : p + 4])
		p += 4
		
		uvIndex, p = parseInteger(s, p)
		
		layerIndices.append(vmap[0])
		uvIndices.append(uvIndex)
	
	
	p += 8
	materialsCount, p = parseShort(s, p) #Количество материалов, используемых объекотм
	
	material_names = [] #Имена материалов, используемых объектом
	triangles_indices = [] #Айдишники треугольников, использующих материал
	
	for i in range(materialsCount):
		materialName, p = parseString(s, p)
		
		material_names.append(materialName)
		
		trianglesCount, p = parseInteger(s, p) #Количество треугольников, использующих этот материал
		
		triangles_indices.append(unpack('%di' % (trianglesCount), s[p : p + 4 * trianglesCount]))
		p += 4 * trianglesCount
	
	p += 8
	uvTablesCount, p = parseInteger(s, p) #Количество таблиц UV-развертки
	
	uvs = []
	for i in range(uvTablesCount):
		currentUv = []
		chanelName, p = parseString(s, p)
		x, p = parseByte(s, p)
		layerIndex, p = parseShort(s, p)
		count, p = parseInteger(s, p)
		
		for j in range(count):
			uv = []
			uv_value, p = parseFloat(s, p)
			uv.append(uv_value)
			uv_value, p = parseFloat(s, p)
			uv.append(uv_value)
			
			currentUv.append(uv)
		uvs.append(currentUv)
		
		for j in range(count):
			x, p = parseInteger(s, p)

	iIter = 0
	while len(s) > p:
		x, p = parseInteger(s, p)
		iIter += 1
		
		'''
		# Как в перл скриптах Бардака (работает с ошибками)
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
				'''
	
	if bpy.ops.object.mode_set.poll():
		bpy.ops.object.mode_set(mode='OBJECT')
	
	
	mesh = bpy.data.meshes.new(name)
	obj = bpy.data.objects.new(name, mesh)
	scene = bpy.context.scene
	scene.objects.link(obj)
	mesh.from_pydata(verts, (), faces)
	for n, mat_name in enumerate(material_names):
		try:
			if bpy.data.materials[mat_name]:
				material = bpy.data.materials[mat_name]
		except:
			material = bpy.data.materials.new(mat_name)
		bpy.context.scene.objects.active = obj
		bpy.ops.object.material_slot_add()
		obj.material_slots[n].material = material
		material.specular_intensity = 0
	
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




#Получить геометрию
def parseGeometryBlock(s):
	p = 0
	while p < len(s):
		i, p = parseInteger(s, p) #Айдишник подобъекта
		dataSize, p = parseInteger(s, p) #Размер подобъекта
		material_names = parseMeshData(s[p : p + dataSize]) #Читаем подобъект и получаем ссылки на его материалы
		p += dataSize   
	return material_names

#Получить материалы
def parseMaterialBlock(s, material_names):
	p = 0
	materialsCount, p = parseInteger(s, p)

	textures = []
	
	
	for i in range(materialsCount):
		materialName, p = parseString(s, p) #Имя(айдишник) материала
		engineShader, p = parseString(s, p) #Игровой шейдер
		compilerShader, p = parseString(s, p) #Компиляционный шейдер
		gameMaterial, p = parseString(s, p) #Игровой материал
		texturePath, p = parseString(s, p) #Путь к текстуре
		texture, p = parseString(s, p) #Неизвестные данные
        
		double_sides, p = parseInteger(s, p) #Объект двухсторонний
        
        
		unknown_data = unpack('8B', s[p : p + 8])[0] #Неизвестные данные
		p += 8
        
		
		path = textures_path + texturePath + '.dds'
		try:
			image_name = path.split('\\')[-1]
			if bpy.data.images[image_name]:
				image = bpy.data.images[image_name]
		except:
			image = bpy.data.images.load(path)
			debug(str(materialName) + ' - ' + str(image))
			
		try:
			if bpy.data.textures[materialName]:
				texture = bpy.data.textures[materialName]
		except:
			texture = bpy.data.textures.new(materialName, type = 'IMAGE')
			texture.image = image
			textures.append((materialName, texture))
	
	for obj in bpy.data.objects:
		is_has_material_by_obj = True #False
		for name, texture in textures:
			if name in obj.material_slots:
				is_has_material_by_obj = True
				try:
					if obj.material_slots[name].material.texture_slots[0].name:
						pass
				except:
					tex_slot = obj.material_slots[name].material.texture_slots.add()
					tex_slot.texture = texture
					tex_slot.texture_coords = 'UV'
		
		
		if is_has_material_by_obj:
			mesh = obj.data
			n = 0
			for i in mesh.polygons:
				mat = i.material_index
				image = obj.material_slots[mat].material.texture_slots[0].texture.image
				obj.data.uv_textures[0].data[n].image = image
				n += 1


#Загрузить объект из файла
def load_object(filename,context):
	f = open(filename, 'rb')
	s = f.read()
	f.close()
	print('import %s' % filename)
    
	p = 8    # 0x7777
        
	while p < len(s):
		#Текущий чанк(блок)
		#Варианты: геометрия(0x0910), материалы(0x0907), авторы(0x0922)
		block, p = parseInteger(s, p)
		blockSize, p = parseInteger(s, p) #Размер текущего блока
        
		if block == 0x0910:
			material_names = parseGeometryBlock(s[p : p + blockSize])
		elif block == 0x0907:
			parseMaterialBlock(s[p : p + blockSize], material_names)
		p += blockSize
	#debug_file.close()
	bpy.context.scene.update()




from bpy.props import StringProperty, BoolProperty


class IMPORT_OT_object(bpy.types.Operator):
	"""Import OBJECT Operator"""
	bl_idname = "import_scene.object"
	bl_label = "Import OBJECT"
	bl_description = "Import a XRay Engine Object file"
	bl_options = {'REGISTER', 'UNDO'}
	filename_ext = ".object"
	filter_glob = StringProperty(
		default = "*.object",
		options = {'HIDDEN'},
	)


	filepath= StringProperty(
		name="File Path",
		description="Filepath used for importing the OBJECT file",
		maxlen=1024,
		default=""
	)

	def execute(self, context):
		load_object(self.filepath, context)
		return {'FINISHED'}

	def invoke(self, context, event):
		wm= context.window_manager
		wm.fileselect_add(self)
		return {'RUNNING_MODAL'}


def menu_func(self, context):
	self.layout.operator(IMPORT_OT_object.bl_idname, text="XRay Engine Object (.object)")


def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_file_import.append(menu_func)


def unregister():
	try:
		bpy.utils.unregister_module(__name__)
	except:
		pass
	try:
		bpy.types.INFO_MT_file_import.remove(menu_func)
	except:
		pass

if __name__ == "__main__":
	unregister()
	register()
	
	

