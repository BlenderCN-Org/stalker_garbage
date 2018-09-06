import math				# Использовал для преобразования радиан в градусы.
from struct import *	# Импорт модуля для распаковки байтов.
f = open(r'c:\1.object', 'rb')	# Импортируемый файл.
s = f.read()					# Прочитать данные файла и записать их в s.
f.close()						# Закрыть импортируемый файл.

def un_i(p):	# Unpack Integer. Функция для распаковки целых чисел из 4 байтов.
	return unpack('I', s[p : p + 4])[0]

def p_geom_b(s):
	p = 4
	while p < len(s):
		data_size = un_i(p)
		p += 4
		#print 'parse_mesh_data'
		p += data_size

def ang(radian):	# convert radian angle
	return round(math.degrees(radian), 1)

def parse_string(s, p):
	string = ''
	b = unpack('B', s[p : p + 1])[0]
	p += 1
	while b != 0:
		string = string + chr(b)
		b = unpack('B', s[p : p + 1])[0]
		p += 1
	return string, p

p = 8
while p < len(s):
	block = un_i(p)
	p += 4
	block_size = un_i(p)
	p += 4

	if block == 0x0900:
		#print 'EOBJ_CHUNK_VERSION = 0x0900'
		version_format = unpack('H', s[p : p + 2])[0]
		if version_format == 16:
			print '\n*.OBJECT Version = SoC \n'
		else:
			print '\n*.OBJECT Version = ??? \n'

	elif block == 0x0903:
		#print 'EOBJ_CHUNK_FLAGS = 0x0903'
		flags = unpack('I', s[p : p + 4])[0]
		print '\nFlags:\n'
		if flags == 3:
			print '\tMake Progressive = True\n'
		elif flags == 1:
			print '\tMake Progressive = False\n'
		else:
			print 'Error Block Flags', block

	elif block == 0x0905:
		print 'EOBJ_CHUNK_SURFACES_0 = 0x0905'
	elif block == 0x0906:
		print 'EOBJ_CHUNK_SURFACES_1 = 0x0906'
	elif block == 0x0907:
		print 'EOBJ_CHUNK_SURFACES_2 = 0x0907'
	elif block == 0x0910:
		print 'EOBJ_CHUNK_MESHES = 0x0910'	# Данные о геометрии.
		p_geom_b(s[p : p + block_size])	# Parse Geometry Block
	elif block == 0x0911:
		print 'EOBJ_CHUNK_0911 = 0x0911'

	elif block == 0x0912:
		#print 'EOBJ_CHUNK_USERDATA = 0x0912'
		user_data = unpack('%ds' % block_size, s[p : p + block_size])
		print '\nUser Data:\n'
		print '\t', str(user_data)[2:-7], '\n'

	elif block == 0x0913:
		print 'EOBJ_CHUNK_BONES_0 = 0x0913'
	elif block == 0x0916:
		print 'EOBJ_CHUNK_MOTIONS = 0x0916'
	elif block == 0x0918:
		print 'EOBJ_CHUNK_SHADERS_0 = 0x0918'
	elif block == 0x0919:
		print 'EOBJ_CHUNK_PARTITIONS_0 = 0x0919'

	elif block == 0x0920:
		#print 'EOBJ_CHUNK_TRANSFORM = 0x0920'
		transform = unpack('6f', s[p : p + 24])
		position = (transform[0], transform[1], transform[2])
		rotation = (ang(transform[3]), ang(transform[4]), ang(transform[5]))
		print '\nTransform:\n'
		print '\tPosition = ', position, '\n'
		print '\tRotation = ', rotation, '\n'

	elif block == 0x0921:
		print 'EOBJ_CHUNK_BONES_1 = 0x0921'

	elif block == 0x0922:
		#print 'EOBJ_CHUNK_REVISION = 0x0922'
		authors = unpack('%ds' % block_size, s[p : p + block_size])
		print '\nAuthor:\n', authors

	elif block == 0x0923:
		print 'EOBJ_CHUNK_PARTITIONS_1 = 0x0923'
	elif block == 0x0924:
		print 'EOBJ_CHUNK_MOTION_REFS = 0x0924'

	elif block == 0x0925:
		#print 'EOBJ_CHUNK_LOD_REF = 0x0925'
		lod = unpack('%ds' % block_size, s[p : p + block_size])
		print '\nLOD Reference:\n'
		print '\t', str(lod)[2:-7], '\n'

	else:
		print 'unknow block'
	p += block_size
raw_input()