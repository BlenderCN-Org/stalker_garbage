#                                           #
#    XRay Engine (S.T.A.L.K.E.R.) object    #
#       export plugin for Blender      #
#                                           #
#          Denis Mikhaylov            #
#                                           #
#               (2014 November)                 #
#                                           #


bl_info = {
	"name": "Export XRay Engine (S.T.A.L.K.E.R.) Objects",
	"author": "Denis Mikhaylov",
	"version": (1, 0),
	"blender": (2, 70, 0),
	"location": "File > Export > XRay Engine Object (.object)",
	"description": "Export a .object file.",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Import-Export"}


import struct
import io
import operator

import os

import bpy
from mathutils import Vector


object_format = {
	"EOBJ_VERSION"				: 0x10,
	
	"EOBJ_CHUNK_MAIN"			: 0x7777,
	"EOBJ_CHUNK_VERSION"		: 0x0900,
	"EOBJ_CHUNK_FLAGS"			: 0x0903,
	"EOBJ_CHUNK_SURFACES_0"		: 0x0905, #old format
	"EOBJ_CHUNK_SURFACES_1"		: 0x0906, #old format
	"EOBJ_CHUNK_SURFACES_2"		: 0x0907,
	"EOBJ_CHUNK_MESHES"			: 0x0910,
	"EOBJ_CHUNK_0911"			: 0x0911, # ignored by AE
	"EOBJ_CHUNK_USERDATA"		: 0x0912,
	"EOBJ_CHUNK_BONES_0"		: 0x0913, #old format
	"EOBJ_CHUNK_MOTIONS"		: 0x0916,
	"EOBJ_CHUNK_SHADERS_0"		: 0x0918, #old format
	"EOBJ_CHUNK_PARTITIONS_0"	: 0x0919, #old format
	"EOBJ_CHUNK_TRANSFORM"		: 0x0920,
	"EOBJ_CHUNK_BONES_1"		: 0x0921,
	"EOBJ_CHUNK_REVISION"		: 0x0922, #file revision
	"EOBJ_CHUNK_PARTITIONS_1"	: 0x0923,
	"EOBJ_CHUNK_MOTION_REFS"	: 0x0924,
	"EOBJ_CHUNK_LOD_REF"		: 0x0925, # LOD\Reference
	
	"EOBJ_CLIP_VERSION_CHUNK"	: 0x9000,
	"EOBJ_CLIP_DATA_CHUNK"		: 0x9001,
	
	"EMESH_VERSION"				: 0x11,
	
	"EMESH_CHUNK_VERSION"		: 0x1000,
	"EMESH_CHUNK_MESHNAME"		: 0x1001,
	"EMESH_CHUNK_FLAGS"			: 0x1002,
	"EMESH_CHUNK_BBOX"			: 0x1004,
	"EMESH_CHUNK_VERTS"			: 0x1005,
	"EMESH_CHUNK_FACES"			: 0x1006,
	"EMESH_CHUNK_VMAPS_0"		: 0x1007,
	"EMESH_CHUNK_VMREFS"		: 0x1008,
	"EMESH_CHUNK_SFACE"			: 0x1009,
	"EMESH_CHUNK_OPTIONS"		: 0x1010,
	"EMESH_CHUNK_VMAPS_1"		: 0x1011,
	"EMESH_CHUNK_VMAPS_2"		: 0x1012,
	"EMESH_CHUNK_SG"			: 0x1013,
	
	"BONE_VERSION_1"			: 0x1,
	
	"BONE_VERSION_2"			: 0x2,
	
	"BONE_VERSION"				: 0x2,
	
	"BONE_CHUNK_VERSION"		: 0x0001,
	"BONE_CHUNK_DEF"			: 0x0002,
	"BONE_CHUNK_BIND_POSE"		: 0x0003,
	"BONE_CHUNK_MATERIAL"		: 0x0004,
	"BONE_CHUNK_SHAPE"			: 0x0005,
	"BONE_CHUNK_IK_JOINT"		: 0x0006,
	"BONE_CHUNK_MASS_PARAMS"	: 0x0007,
	"BONE_CHUNK_IK_FLAGS"		: 0x0008,
	"BONE_CHUNK_BREAK_PARAMS"	: 0x0009,
	"BONE_CHUNK_FRICTION"		: 0x0010
}


class vector2:
	x = 0
	y = 0
	
	def set(_x, _y):
		x = _x
		y = _y

class vector3:
	x = 0
	y = 0
	z = 0
	
	def set(_x, _y, _z):
		x = _x
		y = _y
		z = _z

class fbox:
	min = vector3()
	max = vector3()
	
	def set(_min, _max):
		min = _min
		max = _max

class lw_options:
	unk1 = 0
	unk2 = 0
	
	def set(_unk1, _unk2):
		unk1 = _unk1
		unk2 = _unk2

class xr_writer:

	UINT8_MAX = 0xff
	UINT16_MAX = 0xffff
	UINT32_MAX = 0xffffffff
	INT16_MAX = 0x7fff
	INT32_MAX = 0x7fffffff
	
	m_open_chunks = []
	m_file = 0
	
	def open_file(self, filename):
		self.m_file = open(filename, 'wb')

	def close_file(self):
		_file = self.m_file
		_file.close()
		
	def seek(self, value):
		_file = self.m_file
		_file.seek(value)
	
	def tell(self):
		_file = self.m_file
		return _file.tell()
	
	def w(self, value, type):
		_file = self.m_file
		_file.write(struct.pack(type, value))
	
	def w_s8(self, value):
		self.w(value, 'b')
	
	def w_s16(self, value):
		self.w(value, 'h')
	
	def w_s32(self, value):
		self.w(value, 'i')
	
	def w_size_s32(self, value):
		self.w_s32(value & self.UINT32_MAX)
	
	def w_size_s16(self, value):
		self.w_s16(value & self.UINT16_MAX)
	
	def w_size_s8(self, value):
		self.w_s8(value & self.UINT8_MAX)
	
	def w_float(self, value):
		self.w(value, 'f')
	
	def w_bool(self, value):
		if value:
			self.w_s8(1)
		else:
			self.w_s8(0)
	
	def w_stringZ(self, value):

		_file = self.m_file
		_file.write(bytes(value, 'UTF-8'))
		_file.write(struct.pack('b', 0))
		
		#s_length = len(value)
		#if s_length > 0:
		#	for i in range(s_length-1):
		#		self.w_s8(int(value[i]))
		#self.w_s8(0)
	
	def w_vector2(self, value):
		self.w_float(value.x)
		self.w_float(value.y)
	
	def w_vector3(self, value):
		self.w_float(value.x)
		self.w_float(value.y)
		self.w_float(value.z)
	
	def w_fbox(self, value):
		self.w_vector3(value.min)
		self.w_vector3(value.max)
	
	def w_lw_options(self, value):
		self.w_s32(value.unk1)
		self.w_s32(value.unk2)
	
	def open_chunk(self, id):
		self.w_s32(id) #Записываем индекс блока
		self.w_s32(0) #Занимаем место для будущего размера блока
		self.m_open_chunks.append(self.tell()) #Сохраняем адрес текущей ячейки, чтобы позднее записать размер
	
	def close_chunk(self):
		_file = self.m_file
		c_length = len(self.m_open_chunks)
		if c_length != 0:
			pos = self.tell()
			chunk_pos = self.m_open_chunks[c_length - 1]
			if chunk_pos <= pos:
				self.seek(chunk_pos - 4)
				self.w_size_s32(pos - chunk_pos)
				self.seek(pos)
				self.m_open_chunks.remove(chunk_pos)
			else:
				print("Error! chunk_pos > pos!")
		else:
			print("Error! Open chunks is empty!")

	def w_chunk(self, type_id, chunk_id, value):
		self.open_chunk(chunk_id)
		self.w(value, type_id)
		self.close_chunk()
	
	def w_chunk_s8(self, chunk_id, value):
		self.w_chunk('b', chunk_id, value)

	def w_chunk_s16(self, chunk_id, value):
		self.w_chunk('h', chunk_id, value)

	def w_chunk_s32(self, chunk_id, value):
		self.w_chunk('i', chunk_id, value)

	def w_chunk_float(self, chunk_id, value):
		self.w_chunk('f', chunk_id, value)

	def w_chunk_stringZ(self, chunk_id, value):
		self.open_chunk(chunk_id)
		self.w_stringZ(value)
		self.close_chunk()

	def w_chunk_vector2(self, chunk_id, value):
		self.open_chunk(chunk_id)
		self.w_vector2(value)
		self.close_chunk()

	def w_chunk_vector3(self, chunk_id, value):
		self.open_chunk(chunk_id)
		self.w_vector3(value)
		self.close_chunk()

	def w_chunk_fbox(self, chunk_id, value):
		self.open_chunk(chunk_id)
		self.w_fbox(value)
		self.close_chunk()

	def w_chunk_lw_options(self, chunk_id, value):
		self.open_chunk(chunk_id)
		self.w_lw_options(value)
		self.close_chunk()

def mesh_triangulate(mesh):
	import bmesh
	bm = bmesh.new()
	bm.from_mesh(mesh)
	bmesh.ops.triangulate(bm, faces=bm.faces)
	bm.to_mesh(mesh)
	bm.free()

def get_verticles(obj):
	mesh = obj.data
	if mesh.vertices:
		nv = [v.co for v in mesh.vertices]
		xx = [ co[0] for co in nv ]
		yy = [ co[1] for co in nv ]
		zz = [ co[2] for co in nv ]
	else:
		xx = yy = zz = [0.0,]
	
	return xx, yy, zz

def calculate_bbox(xx, yy, zz):
	value = fbox()
	
	value.min.x = min(xx)
	value.min.y = min(yy)
	value.min.z = min(zz)
	
	value.max.x = max(xx)
	value.max.y = max(yy)
	value.max.z = max(zz)
	
	return value
	

def save_chunk_main_meshes_verts(packet, xx, yy, zz):
	length = len(xx)
	packet.w_size_s32(length)
	for i in range(length):
		packet.w_float(xx[i])
		packet.w_float(zz[i])
		packet.w_float(yy[i])
	

def save_chunk_main_meshes_faces(packet, obj):

	mesh = obj.data
	
	used_verticles = {}
	vertices_by_loop = {}
	loop_cnt = 0
	loop_second_cnt = 0
	
	length = len(mesh.polygons)
	packet.w_size_s32(length)
	
	for i in range(length):
	
		ver = mesh.polygons[i].vertices
		loop = mesh.polygons[i].loop_indices
		
		for j in range(3):
			vertices_by_loop[loop[j]] = {}
			vertices_by_loop[loop[j]][0] = ver[j]
			# vertices_by_loop[loop[j]][1] = Вертекс дублирован?
			vertices_by_loop[loop[j]][2] = mesh.polygons[i]
			vertices_by_loop[loop[j]][3] = j
			if ver[j] in used_verticles and used_verticles[ver[j]] == True:
				vertices_by_loop[loop[j]][1] = True
				loop_second_cnt += 1
			else:
				vertices_by_loop[loop[j]][1] = False
				used_verticles[ver[j]] = True
			loop_cnt += 1
		
		#vertices_by_loop[loop[0]] = ver[0]
		#vertices_by_loop[loop[1]] = ver[1]
		#vertices_by_loop[loop[2]] = ver[2]
		
		packet.w_s32(ver[0])
		packet.w_s32(loop[0])
		packet.w_s32(ver[1])
		packet.w_s32(loop[1])
		packet.w_s32(ver[2])
		packet.w_s32(loop[2])

	
	return vertices_by_loop, loop_cnt, loop_second_cnt

def save_chunk_main_meshes_sg(packet, obj):
	
	mesh = obj.data
	
	smooth_groups, smooth_groups_tot = mesh.calc_smooth_groups(True)
	
	length = len(mesh.polygons)
	
	for i in range(length):
		if i in smooth_groups:
			packet.w_s32(smooth_groups[i])
		else:
			packet.w_s32(0)
	

def save_chunk_main_meshes_vmrefs(packet, obj, vertices_by_loop, loop_cnt):
	
	mesh = obj.data

	packet.w_size_s32(loop_cnt)
	
	vetrices_id = 0
	
	for i in range(loop_cnt):
		
		packet.w_s8(1)
		if vertices_by_loop[i][1] == False:
			packet.w_s32(0)
			packet.w_s32(vertices_by_loop[i][0])
		else:
			packet.w_s32(1)
			packet.w_s32(vetrices_id)
			vetrices_id += 1
		
	

def save_chunk_main_meshes_sface(packet, obj):
	
	mesh = obj.data
	
	length = len(obj.material_slots)
	
	packet.w_size_s16(length)
	
	for i in range(length):
		this_material = obj.material_slots[i].material
		packet.w_stringZ(this_material.name)
		
		face_cnt = 0
		faces = []
		
		for face in mesh.polygons:
			if face.material_index == i:
				faces.append(face.index)
				face_cnt += 1
		
		packet.w_size_s32(face_cnt)
		
		for face_id in faces:
			packet.w_s32(face_id)
	

def save_chunk_main_meshes_vmaps_2(packet, obj, vertices_by_loop, loop_cnt, loop_second_cnt):
	
	mesh = obj.data
	
	UVCoordinates = mesh.uv_layers.active.data
	
	packet.w_size_s32(2)
	
	packet.w_stringZ("Texture")
	packet.w_s8(2)
	packet.w_s16(0)

	uv_by_vertices = {}
	
	for polygon in mesh.polygons:
		
		uv_by_vertices[polygon.vertices[0]] = UVCoordinates[polygon.loop_indices[0]]
		uv_by_vertices[polygon.vertices[1]] = UVCoordinates[polygon.loop_indices[1]]
		uv_by_vertices[polygon.vertices[2]] = UVCoordinates[polygon.loop_indices[2]]
	
	length = len(uv_by_vertices)
	
	packet.w_size_s32(length)
	for i in range(length):
		packet.w_float(uv_by_vertices[i].uv[0])
		packet.w_float((uv_by_vertices[i].uv[1]*-1.0)-1.0)
	
	
	for i in range(length):
		packet.w_s32(i)
	
	
	packet.w_stringZ("Texture")
	packet.w_s8(2)
	packet.w_s16(1)

	packet.w_size_s32(loop_second_cnt)
	
	for i in range(loop_cnt):
		
		if vertices_by_loop[i][1] == True:
			polygon = vertices_by_loop[i][2]
			map = UVCoordinates[polygon.loop_indices[vertices_by_loop[i][3]]]
			packet.w_float(map.uv[0])
			packet.w_float((map.uv[1]*-1.0)-1.0)
		
	
	for i in range(loop_cnt):
		if vertices_by_loop[i][1] == True:
			packet.w_s32(vertices_by_loop[i][0])
		
	
	for i in range(loop_cnt):
		if vertices_by_loop[i][1] == True:
			packet.w_s32(vertices_by_loop[i][2].index)
		
	
	

def save_chunk_main_mesh(packet, obj):
	
	mesh_triangulate(obj.data)
	
	xx, yy, zz = get_verticles(obj)

	options = lw_options()
	bbox = calculate_bbox(xx, yy, zz)
	
	packet.w_chunk_s16(object_format['EMESH_CHUNK_VERSION'], object_format['EMESH_VERSION'])
	packet.w_chunk_stringZ(object_format['EMESH_CHUNK_MESHNAME'], obj.name)
	packet.w_chunk_fbox(object_format['EMESH_CHUNK_BBOX'], bbox)
	packet.w_chunk_s8(object_format['EMESH_CHUNK_FLAGS'], 0x01)
	packet.w_chunk_lw_options(object_format['EMESH_CHUNK_OPTIONS'], options)
	
	packet.open_chunk(object_format['EMESH_CHUNK_VERTS'])
	save_chunk_main_meshes_verts(packet, xx, yy, zz)
	packet.close_chunk()
	
	packet.open_chunk(object_format['EMESH_CHUNK_FACES'])
	vertices_by_loop, loop_cnt, loop_second_cnt = save_chunk_main_meshes_faces(packet, obj)
	packet.close_chunk()
	
	packet.open_chunk(object_format['EMESH_CHUNK_SG'])
	save_chunk_main_meshes_sg(packet, obj)
	packet.close_chunk()
	
	packet.open_chunk(object_format['EMESH_CHUNK_VMREFS'])
	save_chunk_main_meshes_vmrefs(packet, obj, vertices_by_loop, loop_cnt)
	packet.close_chunk()
	
	packet.open_chunk(object_format['EMESH_CHUNK_SFACE'])
	save_chunk_main_meshes_sface(packet, obj)
	packet.close_chunk()
	
	packet.open_chunk(object_format['EMESH_CHUNK_VMAPS_2'])
	save_chunk_main_meshes_vmaps_2(packet, obj, vertices_by_loop, loop_cnt, loop_second_cnt)
	packet.close_chunk()
	

def save_chunk_main_meshes(packet):
	
	iID = 0
	for obj in bpy.data.objects:
		if obj.type == 'MESH':
			mesh = obj.data
			
			if len(mesh.polygons) >= 1 and len(mesh.vertices) >= 1:
				packet.open_chunk(iID)
				save_chunk_main_mesh(packet, obj)
				packet.close_chunk()
				iID += 1
			else:
				print("Error! Scene has single vertices!")
	

ESURFACE_DEFAULT_FVF = 0x112

def get_texture_name(texture_name):
	
	new_texture_name = ''
	b = False
	
	for i in range(len(texture_name)):
		if texture_name[i] == '_' and b == False:
			_name = new_texture_name
			b = True
			new_texture_name += '\\'
			new_texture_name += _name
			new_texture_name += '_'
		elif b == False:
			new_texture_name += str(texture_name[i])
		elif b == True:
			if texture_name[i] == '.':
				break
			else:
				new_texture_name += str(texture_name[i])
	
	return new_texture_name

def save_chunk_main_surfaces_2(packet):
	
	packet.w_size_s32(len(bpy.data.materials))
	
	for material in bpy.data.materials:
	
		texture_name = get_texture_name(material.active_texture.image.name)
		
		packet.w_stringZ(material.name)
		packet.w_stringZ("default")
		packet.w_stringZ("default")
		packet.w_stringZ("default")
		packet.w_stringZ(texture_name)
		packet.w_stringZ("Texture")
		packet.w_s32(0)
		packet.w_s32(ESURFACE_DEFAULT_FVF)
		packet.w_s32(1)
	

def save_chunk_main_revision(packet):
	
	packet.w_stringZ("unknown")
	packet.w_s32(0)
	packet.w_stringZ("unknown")
	packet.w_s32(0)
	

def save_chunk_main(packet):

	packet.w_chunk_s16(object_format['EOBJ_CHUNK_VERSION'], object_format['EOBJ_VERSION'])
	packet.w_chunk_stringZ(object_format['EOBJ_CHUNK_USERDATA'], '')
	packet.w_chunk_stringZ(object_format['EOBJ_CHUNK_LOD_REF'], '')
	packet.w_chunk_s32(object_format['EOBJ_CHUNK_FLAGS'], 0x0)
	
	packet.open_chunk(object_format['EOBJ_CHUNK_MESHES'])
	save_chunk_main_meshes(packet)
	packet.close_chunk()
	
	packet.open_chunk(object_format['EOBJ_CHUNK_SURFACES_2'])
	save_chunk_main_surfaces_2(packet)
	packet.close_chunk()
	
	packet.open_chunk(object_format['EOBJ_CHUNK_REVISION'])
	save_chunk_main_revision(packet)
	packet.close_chunk()
	

def save_object(filepath, context):
	
	packet = xr_writer()
	packet.open_file(filepath)
	
	packet.open_chunk(object_format['EOBJ_CHUNK_MAIN'])
	save_chunk_main(packet)
	packet.close_chunk()
	
	packet.close_file()
	
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ExportHelper


class ObjectExport(bpy.types.Operator, ExportHelper):
	"""Export OBJECT Operator"""
	bl_idname = "export.object"
	bl_label = "ObjectExport"
	bl_description = "Export XRay Engine Object file"
	bl_options = {"REGISTER"}
	filename_ext = ".object"
	filter_glob = StringProperty(
		default = "*.object",
		options = {'HIDDEN'}
	)

	filepath = StringProperty( 
		name = "File Path",
		description = "File path used for exporting the OBJECT file",
		maxlen = 1024,
		default = ""
	)

	def execute(self, context):
		
		global main
		
		main = self
	
		self.context = context
		self.VCOL_NAME = "Per-Face Vertex Colors"
		self.DEFAULT_NAME = "Blender Default"
		
		if struct and io and operator:
			save_object(self.filepath, context)
		else:
			bpy.ops.ObjectExport.message('INVOKE_DEFAULT')
		
		
		return {'FINISHED'}
	
	def invoke(self, context, event):
		wm= context.window_manager
		wm.fileselect_add(self)
		return {'RUNNING_MODAL'}



def menu_func(self, context):
	self.layout.operator(ObjectExport.bl_idname, text="XRay Engine Object (.object)")

	
def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_file_export.append(menu_func)

	
def unregister():
	try:
		bpy.utils.unregister_module(__name__)
	except:
		pass
	try:
		bpy.types.INFO_MT_file_export.remove(menu_func)
	except:
		pass

if __name__ == "__main__":
	unregister()
	register()


