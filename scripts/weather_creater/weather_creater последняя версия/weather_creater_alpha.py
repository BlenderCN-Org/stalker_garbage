def s(file, path_mode = False):
	"""
	Функция считывает 1 текстовую строку из файла file.
	"""
	if path_mode == True:		# режим чтения пути из файла
		string = file.readline()
		if string[-1] == '\n':		# в пути не должно быть абзацев
			string = string[:-1]
	else:
		# используется eval для сохранения \n и \t в тексте
		string = eval(file.readline())
	return string

def si(text, o):		# string input
	"""
	Функция возвращает введённую с клавиатуры строку.
	text - подсказка при вводе
	o - режим ввода
		0 - строка
		1 - y или n
		2 - целое число
		3 - дробное число
	"""
	string = input(text)
	if o == 1:			# Y/N
		otvet = None
		if string.upper() == 'Y':
			otvet = True
		elif string.upper() == 'N':
			otvet = False
		else:
			print(t_y_or_n)
		return otvet
	elif o == 2:		# INT
		try:
			integer = int(string)
		except:
			print('Введите целое число!')
		return integer
	elif o == 3:		# FLOAT
		try:
			number = float(string)
		except:
			print('Введите дробное число!')
		return number
	else:
		return string

file_path = open(r'path.txt', 'r')			# файл с путями
path_base_t = s(file_path, True)#file_path.readline()[:-1]		# путь к базовым текстам
path_long_t = s(file_path, True)		# путь к полным текстам
path_short_t = s(file_path, True)	# путь к кратким текстам
file_path.close()							# закрыть файл с путями, он уже не нужен
### базовые тексты ###
b = open(path_base_t, 'r')	# файл содержит базовые тексты
# тексты программы начинаются с префикса t_ (для удобства)
t_about = s(b)
t_help = s(b)
t_y_or_n = s(b)
t_hp_te = s(b)
t_hp_false = s(b)
n = '\n'
b.close()		# закрыть базовые тексты. они уже не нужны
### базовые тексты ###

print('{0}{1}{0}{2}'.format('='*71, t_about, t_help))		#Описание программы
# Опции
run_help = True		# условие цикличного запроса ответа
help_on = None		# условие включения подробных подсказок
while run_help:
	helper = si('', 1)		# запустить с подсказками или нет
	if helper == True:
		run_help = False
		help_on = True
		print(t_hp_te)
	elif helper == False:
		run_help = False
		help_on = False
		print(t_hp_false)
	else:
		pass

if help_on:
	f = open(path_long_t, 'r')
else:
	f = open(path_short_t, 'r')

### Тексты ###
t_path = s(f)
t_path_default = s(f)
t_save = s(f)
t_name = s(f)
t_amb_m = s(f)
t_amb_m_r = s(f)
t_amb_m_g = s(f)
t_amb_m_b = s(f)
t_amb_b = s(f)
t_amb_b_r = s(f)
t_amb_b_g = s(f)
t_amb_b_b = s(f)
t_hemi = s(f)
t_hemi_m_r = s(f)
t_hemi_m_g = s(f)
t_hemi_m_b = s(f)
t_hemi_b = s(f)
t_hemi_b_r = s(f)
t_hemi_b_g = s(f)
t_hemi_b_b = s(f)
t_scale_amb = s(f)
t_scl_amb_val = s(f)
t_scale_hemi = s(f)
t_scl_hemi_val = s(f)
t_night = s(f)
t_day = s(f)
t_rassvet = s(f)
t_zakat = s(f)
f.close()		# закрыть файл с текстами. он уже не нужен
### Тексты ###

path = si(t_path, 0)	# указывается путь сохранения файла с погодой
# путь по-умолчанию или указанный
if str(path) == ' ':
	print(t_path_default)
	path = 'C:\weather_test.ltx'	# путь соханения файла с погодой
else:
	print(t_save, path, n)

file = open(path, 'w')		# создаётся файл погоды
weather_name = si(t_name, 0)		#Задаётся имя секции погоды
file.write('[sect_{0}]\n\n'.format(weather_name))

#Запись времени и секций, которые соответствуют данному времени
i = 0
while i < 10:		# в этом цикле добавляется ноль перед i, т.к. i двузначное число
	file.write('0{0}:00:00\t\t=\t{1}_0{0}\n'.format(i, weather_name))	# здесь ноль добавляется
	i += 1
while i >= 10 and i < 24:
	file.write('{0}:00:00\t\t=\t{1}_{0}\n'.format(i, weather_name))	# здесь ноль отсутствует
	i += 1
del i
file.write(n)

#AMBIENT
	#Min
ambient_min_r = si(t_amb_m + t_amb_m_r + 'Red = ', 3)
ambient_min_g = si(t_amb_m_g + 'Green = ', 3)
ambient_min_b = si(t_amb_m_b + 'Blue = ', 3)
	#Max
ambient_max_r = si(t_amb_b + t_amb_b_r + 'Red = ', 3)
ambient_max_g = si(t_amb_b_g + 'Green = ', 3)
ambient_max_b = si(t_amb_b_b + 'Blue = ', 3)
#HEMI COLOR
	#Min
hemi_color_min_r = si(t_hemi + t_hemi_m_r + 'Red = ', 3)
hemi_color_min_g = si(t_hemi_m_g + 'Green = ', 3)
hemi_color_min_b = si(t_hemi_m_b + 'Blue = ', 3)
	#Max
hemi_color_max_r = si(t_hemi_b + t_hemi_b_r + 'Red = ', 3)
hemi_color_max_g = si(t_hemi_b_g + 'Green = ', 3)
hemi_color_max_b = si(t_hemi_b_b + 'Blue = ', 3)
#Масштабировать ambient
scale_ambient_option = si(t_scale_amb, 1)
if scale_ambient_option == True:
	scale_ambient = si(t_scl_amb_val, 3)
	ambient_min_r = ambient_min_r * scale_ambient
	ambient_min_g = ambient_min_g * scale_ambient
	ambient_min_b = ambient_min_b * scale_ambient
	ambient_max_r = ambient_min_r * scale_ambient
	ambient_max_g = ambient_min_g * scale_ambient
	ambient_max_b = ambient_min_b * scale_ambient
#Масштабировать hemi_color
scale_hemi_option = si(t_scale_hemi, 1)
if scale_hemi_option == True:
	scale_hemi = si(t_scl_hemi_val, 3)
	hemi_color_min_r = hemi_color_min_r * scale_hemi
	hemi_color_min_g = hemi_color_min_g * scale_hemi
	hemi_color_min_b = hemi_color_min_b * scale_hemi
	hemi_color_max_r = hemi_color_min_r * scale_hemi
	hemi_color_max_g = hemi_color_min_g * scale_hemi
	hemi_color_max_b = hemi_color_min_b * scale_hemi
night = si(t_night, 2)		#Самое темное время
day = si(t_day, 2)			#Самое ясное время
#Постоянные параметры
v1 = ('flares\t\t\t=\tflares_sun_rise\n'
'sky_texture\t\t=\tsky\sky_11_cube\n'
'sky_rotation\t=\t0\n'
'sky_color\t\t=\t1.0,\t1.0,\t1.0\n'
'clouds_texture\t=\tsky\sky_oblaka\n'
'clouds_color\t=\t0.0, 0.0, 0.0, 0.0, 0.0\n'
'far_plane\t\t=\t2000\n'
'fog_distance\t=\t2000\n'
'fog_color\t\t=\t0.0, 0.0, 0.0\n'
'fog_density\t\t=\t0.0\n'
'rain_density\t=\t0.0\n'
'rain_color\t\t=\t0.0, 0.0, 0.0\n'
'thunderbolt\t\t= \t\n'
'bolt_period\t\t=\t4.5f\n'
'bolt_duration\t=\t0.35f\n'
'wind_velocity\t=\t0.0\n'
'wind_direction\t=\t0.0\n')
v2 = ('\nsun_color\t\t=\t0.0, 0.0, 0.0\n'
'lmap_color\t\t=\t1.0,\t1.0,\t1.0\n'
'sun_dir\t\t\t=\t-30.0, 270\n'
'env_ambient\t\t=\tambient_env_tuman\n')
# СБОР ДАННЫХ ЗАКОНЧИЛСЯ
# ДАЛЬШЕ ИДУТ ВЫЧИСЛЕНИЯ
# вычисление шага
step1 = (ambient_max_r - ambient_min_r)/(day - night)
if step1 < 0:
	step1 = step1 * (-1)
print(step1)
#ИЗМЕНИТЬ ШАГ НА ПРАВИЛЬНЫЙ
step2 = (ambient_max_r - ambient_min_r)/(24 - day - night)
if step2 < 0:
	step2 = step2 * (-1)
print(step2)
#Запись параметров в файл
i = 0
while i < 24:
	if i < 10:
		prefix = '0' + str(i)
	else:
		prefix = str(i)

	if (i + 1) > night and (i + 1) < day:
		ambient_r = str(step1*i + ambient_min_r)
		ambient_g = str(step1*i + ambient_min_g)
		ambient_b = str(step1*i + ambient_min_b)
		hemi_color_r = str(step1*i + hemi_color_min_r)
		hemi_color_g = str(step1*i + hemi_color_min_g)
		hemi_color_b = str(step1*i + hemi_color_min_b)

	else:
		ambient_r = str(ambient_max_r - step2*i)
		ambient_g = str(ambient_max_g - step2*i)
		ambient_b = str(ambient_max_b - step2*i)
		hemi_color_r = str(hemi_color_max_r - step2*i)
		hemi_color_g = str(hemi_color_max_g - step2*i)
		hemi_color_b = str(hemi_color_max_b - step2*i)
	len_value = 5
	file.write('[' + str(weather_name) + '_' + str(prefix) + ']\n' + 'ambient\t\t\t=\t' + ambient_r[0:len_value] + ',\t' + ambient_g[0:len_value] + ',\t' + ambient_b[0:len_value] + '\nhemi_color\t\t=\t' + hemi_color_r[0:len_value] + ',\t' + hemi_color_g[0:len_value] + ',\t' + hemi_color_b[0:len_value] + '\n'*2)
	i += 1

file.close()
input()