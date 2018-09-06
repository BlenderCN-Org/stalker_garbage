from struct import *
f = open(r'det_list_01.object', 'rb')
s = f.read()
f.close()


def parse_verts(s):
	p = 0
	verts_count = unpack('i', s[p : p + 4])[0]
	p += 4
	for i in list(range(verts_count)):
		verts = unpack('3f', s[p : p + 12])
		p += 12
		print('\t', verts)
	print('\tVertex Count =', verts_count)

def parse_faces(s):
	p = 0
	faces_count = unpack('i', s[p : p + 4])[0]
	p += 4
	print('\tFaces Count =', faces_count)
	for i in list(range(faces_count)):
		faces = unpack('6i', s[p : p + 24])
		p += 24
		print('\t', faces)

def uv_index(s):
	p = 0
	count = unpack('i', s[p : p + 4])[0]
	p += 4
	print('\tcount =', count)
	for i in list(range(count)):
		unknow = unpack('5b', s[p : p + 5])
		p += 5
		uv_index = unpack('i', s[p : p + 4])[0]
		p += 4
		print('\tUV Index:', uv_index)

def parse_uv(s):
	p = 0
	uv_count = unpack('i', s[p : p + 4])[0]
	p += 4
	print('UV Count =', uv_count)
	uvs = []
	for i in list(range(uv_count)):
		chanel_name = ''
		b = unpack('B', s[p : p + 1])[0]
		p += 1
		while b != 0:
			chanel_name = chanel_name + chr(b)
			b = unpack('B', s[p : p + 1])[0]
			p += 1
		print('chanel name =', chanel_name)
		p += 1	# UNKNOW

def parse_mesh(s):
	p = 0
	block_id = unpack('i', s[p : p + 4])[0]
	p += 4
	block_size = unpack('i', s[p : p + 4])[0]
	p += 4
	while p < len(s):
		block_id = unpack('i', s[p : p + 4])[0]
		p += 4
		block_size = unpack('i', s[p : p + 4])[0]
		p += 4
		print('\n\tblock id = %s,\tblock size = %s\n' % (hex(block_id), block_size))
		if block_id == 0x1000:
			EMESH_CHUNK_VERSION = str(unpack('2s', s[p : p + 2])[0])
			print('\tVersion mesh', EMESH_CHUNK_VERSION[2:-1])
		elif block_id == 0x1001:
			EMESH_CHUNK_MESHNAME = str(unpack('%ds' % block_size, s[p : p + block_size])[0])
			print('\tMesh Name:', EMESH_CHUNK_MESHNAME[2:-5])
		elif block_id == 0x1002:
			EMESH_CHUNK_FLAGS = str(unpack('s', s[p : p + 1])[0])
			print('\tFlags:\t', EMESH_CHUNK_FLAGS[2:-1])
		elif block_id == 0x1004:
			bbox = unpack('6f', s[p : p + 24])
			print('\tbbox min:\n\t', bbox[:3])
			print('\tbbox max:\n\t', bbox[3:])
		elif block_id == 0x1005:
			parse_verts(s[p : p + block_size])
		elif block_id == 0x1006:
			parse_faces(s[p : p + block_size])
		elif block_id == 0x1008:
			uv_index(s[p : p + block_size])
		elif block_id == 0x1010:
			EMESH_CHUNK_OPTIONS = str(unpack('%ds' % block_size, s[p : p + block_size])[0])
			print('\tOptions:\t', EMESH_CHUNK_OPTIONS[2:-1])
		elif block_id == 0x1012:
			parse_uv(s[p : p + block_size])
		elif block_id == 0x1013:
			smooth_grops = unpack('%di' % (block_size / 4), s[p : p + block_size])
			print('\tSmooth Groups = \n\t', smooth_grops)

		p += block_size

def parse_string(s, p):
	string = ''
	ch = unpack('s', s[p : p + 1])[0]
	p += 1
	while ch != b'\x00':
		string = string + str(ch)[2:-1]
		ch = unpack('s', s[p : p + 1])[0]
		p += 1
	print('\t', string, sep = '')
	return string, p

def parse_material(s):
	p = 0
	materials_count = unpack('i', s[p : p + 4])[0]
	p += 4
	print('\tmaterial count = {0}\n'.format(materials_count))
	for i in list(range(materials_count)):
		material_name, p = parse_string(s, p)
		engine_shader, p = parse_string(s, p)
		compiler_shader, p = parse_string(s, p)
		game_material, p = parse_string(s, p)
		texture_path, p = parse_string(s, p)
		texture, p = parse_string(s, p)
		two_sided = unpack('i', s[p : p + 4])[0]
		if two_sided == 0:
			print('\t2 sided = False')
		elif two_sided == 1:
			print('\t2 sided = True')
		else:
			print('\tERROR! 2 sided =', two_sided)	# 2 sided, ?, ?
		p += 4
		unknow_data = unpack('ii', s[p : p + 8])
		print('UNKNOW DATA = {0}\n'.format(unknow_data))
		p += 8

p = 0
block_id = unpack('i', s[p : p + 4])[0]
p += 4
block_size = unpack('i', s[p : p + 4])[0]
p += 4
print('\nheader = {0},\tdata size = {1}\n'.format(hex(block_id), block_size))
file_size = str(block_size + 8)
print('*.OBJECT file ({0}.{1} KB):\n'.format(file_size[:-3], file_size[-3:]))
while p < len(s):
	block_id = unpack('i', s[p : p + 4])[0]
	p += 4
	block_size = unpack('i', s[p : p + 4])[0]
	p += 4
	print('\nblock id = %s,\tblock size = %s\n' % (hex(block_id), block_size))
	if block_id == 0x0900:
		EOBJ_CHUNK_VERSION = str(unpack('b', s[p : p + 1])[0])
		print('\tEOBJ_CHUNK_VERSION:', EOBJ_CHUNK_VERSION)
	elif block_id == 0x0903:
		EOBJ_CHUNK_FLAGS = str(unpack('4s', s[p : p + 4])[0])[2:-1]
		print('\tEOBJ_CHUNK_FLAGS:', EOBJ_CHUNK_FLAGS)
	elif block_id == 0x907:
		parse_material(s[p : p + block_size])
	elif block_id == 0x910:
		parse_mesh(s[p : p + block_size])
	elif block_id == 0x912:
		EOBJ_CHUNK_USERDATA = str(unpack('%ds' % (block_size), s[p : p + block_size])[0])[2:-5]
		print('\tUser Data:\n\t', EOBJ_CHUNK_USERDATA)
	elif block_id == 0x922:
		EOBJ_CHUNK_REVISION = unpack('%ds' % block_size, s[p : p + block_size])[0]
		print('\tAuthors:\n\t', EOBJ_CHUNK_REVISION)
		time = (unpack('4b',(s[p + 14 : p + 18])))
		i = 0
		print('\tcreate data:\n\t', end = '')
		while i < len(time):
			print(hex(time[i]), end = ', ')
			i += 1
	elif block_id == 0x925:
		EOBJ_CHUNK_LOD_REF = str(unpack('%ds' % (block_size), s[p : p + block_size])[0])[2:-5]
		print('\tLOD reference:\n\t', EOBJ_CHUNK_LOD_REF)
	p += block_size
input()
