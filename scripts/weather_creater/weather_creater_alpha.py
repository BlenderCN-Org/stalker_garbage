# -*- coding: utf-8 -*-

# Python 2.6

ru = lambda x:x.decode('utf-8')

### Тексты ###
t_about = ru('\n\t\tЭто программа для создания \n\n\tсекций погоды игры S.T.A.L.K.E.R. Shadows of Chernobyl\n\n')
t_help = ru('Запустить программу с подсказками? \n(Рекомендуется при первом запуске). \nКлавиша \'Y\' - да\nКлавиша \'N\' - нет')
t_y_or_n = (ru('Введите Y или N:'))
t_hp_true = ru('Программа запущена с подсказками\n')
t_hp_false = ru('Программа запущена без подсказок\n')
### Тексты ###

#Описание программы
print '='* 71
print t_about
print '=' * 71, '\n' * 2
print t_help

#Функция для цикличного запуска выбора опции, в случае неверного ввода
def cycle_run_help_option():
	return helper_option()

#Опции
def helper_option():
	print t_y_or_n
	helper = raw_input('\n')
	print
	if str(helper) == 'Y' or str(helper) == 'y':
		local_help_on = 1
		return local_help_on
		print t_hp_true
	elif str(helper) == 'N' or str(helper) == 'n':
		local_help_on = 0
		return local_help_on
		print t_hp_false
	else:
		cycle_run_help_option()
	

help_on = cycle_run_help_option()

### Тексты ###
if help_on == 1:
	t_path = ru('Укажите путь и имя файла, в который нужно сохранить параметры погоды.\nНапример, c:\\name.ltx\n'
	'Если указано имя без пути, то файл будет сохранён в папке, \nиз которой была запущена эта программа.'
	'\nИли нажмите клавишу пробел, для сохранения файла \nв дирректорию по-умолчанию (C:\Weather_Test.ltx).\n'
	'Подтвердите свой выбор, нажав Enter.\n')
	t_path_default = ru('Выбрана дирректория по-умолчанию.\n')
	t_save = ru('\nФайл будет сохранён в ')
	t_name = ru('Введите имя погоды. \nПриставка sect_ будет добавлена автоматически.\n')
	t_amb_m = ru('\nУкажите минимальное значение ambient. '
	'\nПодсказка: ambient подсвечивает всю геометрию уровня в одинаковой степени, \n'
	'не обращая внимания на карты освещения и карты теней. \n'
	'Рекомендуется указать в пределах от 0.01 до 0.1 \n'
	'(дробную часть отделять точкой, а не запятой)')
	t_amb_m_r = ru('\nВведите минимальное значение красного цвета в параметре ambient')
	t_amb_m_g = ru('\nВведите минимальное значение зелёного цвета в параметре ambient')
	t_amb_m_b = ru('\nВведите минимальное значение синего цвета в параметре ambient')
	t_amb_b = ru('\nУкажите максимальное значение ambient.')
	t_amb_b_r = ru('\nВведите максимальное значение красного цвета в параметре ambient')
	t_amb_b_g = ru('\nВведите максимальное значение зелёного цвета в параметре ambient')
	t_amb_b_b = ru('\nВведите максимальное значение синего цвета в параметре ambient')
	t_hemi = ru('\nУкажите минимальное значение hemi_color. '
	'\nПодсказка: hemi_color затеняет труднодоступные для света участки \n(помещения, навесы и т.д.). \n'
	'Рекомендуется указать в пределах от 0.1 до 1.0 \n'
	'(дробную часть отделять точкой, а не запятой)')
	t_hemi_m_r = ru('\nВведите минимальное значение красного цвета в параметре hemi_color')
	t_hemi_m_g = ru('\nВведите минимальное значение зелёного цвета в параметре hemi_color')
	t_hemi_m_b = ru('\nВведите минимальное значение синего цвета в параметре hemi_color')
	t_hemi_b = ru('\nУкажите максимальное значение hemi_color.')
	t_hemi_b_r = ru('\nВведите максимальное значение красного цвета в параметре hemi_color')
	t_hemi_b_g = ru('\nВведите максимальное значение зелёного цвета в параметре hemi_color')
	t_hemi_b_b = ru('\nВведите максимальное значение синего цвета в параметре hemi_color')
	t_scale_amb = ru('\nОтмасштабировать параметр ambient?\nY - да, N - нет.')
	t_scl_amb_val = ru('\nУкажите коэффициент масштабирования.\nЕсли равен 2, то значения изменятся с (1.0, 0.5, 0.25) на (2.0, 1.0, 0.5)')
	t_scale_hemi = ru('\nОтмасштабировать параметр hemi_color?\n'
	'Y - да, N - нет.')
	t_scl_hemi_val = ru('\nУкажите коэффициент масштабирования.')
	t_night = ru('\nУкажите самое тёмное время суток (от 1 до 24):')
	t_day = ru('\nУкажите самое светлое время суток (от 1 до 24):')
	t_rassvet = ru('\nУкажите время рассвета (от 1 до 24):')
	t_zakat = ru('\nУкажите время заката (от 1 до 24):')
else:
	t_path = ru('Путь:')
	t_path_default = ''
	t_save = ''
	t_name = ru('Имя погоды:')
	t_amb_m = ru('Min ambient')
	t_amb_m_r = ru('')
	t_amb_m_g = ru('')
	t_amb_m_b = ru('')
	t_amb_b = ru('Max ambient')
	t_amb_b_r = ru('')
	t_amb_b_g = ru('')
	t_amb_b_b = ru('')
	t_hemi = ru('Min hemi_color')
	t_hemi_m_r = ru('')
	t_hemi_m_g = ru('')
	t_hemi_m_b = ru('')
	t_hemi_b = ru('Max hemi_color')
	t_hemi_b_r = ru('')
	t_hemi_b_g = ru('')
	t_hemi_b_b = ru('')
	t_scale_amb = ru('Scale ambient? Y/N')
	t_scl_amb_val = ru('Scale = ')
	t_scale_hemi = ru('Scale hemi_color? Y/N')
	t_scl_hemi_val = ru('Scale = ')
	t_night = ru('Тёмное время (1-24)')
	t_day = ru('Светлое время (1-24)')
	t_rassvet = ru('Рассвет (1-24):')
	t_zakat = ru('Закат (1-24)')
### Тексты ###

#Указывается путь сохранения файла с погодой
print t_path
path = raw_input()

#Путь по-умолчанию или указанный
if str(path) == ' ':
	print t_path_default
	path = 'C:\Weather_Test.ltx'
else:
	print t_save, path, '\n'

file = open (str(path), 'w')

#Задаётся имя секции погоды
print t_name
weather_name = raw_input()
file.write('[' + 'sect_' + str(weather_name) + ']' + '\n\n')

#Запись времени и секций, которые соответствуют данному времени
i0 = 0
while i0 < 10:
	file.write('0' + str(i0) + ':00:00\t\t=\t' + str(weather_name) + '_' + '0' + str(i0) + '\n')
	i0 += 1
while i0 > 9 and i0 < 24:
	file.write(str(i0) + ':00:00\t\t=\t' + str(weather_name) + '_' + str(i0) + '\n')
	i0 += 1
file.write('\n')

#Ambient
	#Min
print t_amb_m
print t_amb_m_r
ambient_min_r = float(raw_input('Red = '))
print t_amb_m_g
ambient_min_g = float(raw_input('Green = '))
print t_amb_m_b
ambient_min_b = float(raw_input('Blue = '))

	#MAx
print t_amb_b
print t_amb_b_r
ambient_max_r = float(raw_input('Red = '))
print t_amb_b_g
ambient_max_g = float(raw_input('Green = '))
print t_amb_b_b
ambient_max_b = float(raw_input('Blue = '))


#Hemi Color
	#Min
print t_hemi
print t_hemi_m_r
hemi_color_min_r = float(raw_input('Red = '))
print t_hemi_m_g
hemi_color_min_g = float(raw_input('Green = '))
print t_hemi_m_b
hemi_color_min_b = float(raw_input('Blue = '))

	#Max
print t_hemi_b
print t_hemi_b_r
hemi_color_max_r = float(raw_input('Red = '))
print t_hemi_b_g
hemi_color_max_g = float(raw_input('Green = '))
print t_hemi_b_b
hemi_color_max_b = float(raw_input('Blue = '))

#Масштабировать ambient
print t_scale_amb
scale_ambient_option = raw_input()
if str(scale_ambient_option) == 'Y' or str(scale_ambient_option) == 'y':
	print t_scl_amb_val
	scale_ambient = float(raw_input())
	ambient_min_r = ambient_min_r * scale_ambient
	ambient_min_g = ambient_min_g * scale_ambient
	ambient_min_b = ambient_min_b * scale_ambient
	ambient_max_r = ambient_min_r * scale_ambient
	ambient_max_g = ambient_min_g * scale_ambient
	ambient_max_b = ambient_min_b * scale_ambient

#Масштабировать hemi_color
print t_scale_hemi
scale_hemi_option = raw_input()
if str(scale_hemi_option) == 'Y' or str(scale_hemi_option) == 'y':
	print t_scl_hemi_val
	scale_hemi = float(raw_input())
	hemi_color_min_r = hemi_color_min_r * scale_hemi
	hemi_color_min_g = hemi_color_min_g * scale_hemi
	hemi_color_min_b = hemi_color_min_b * scale_hemi
	hemi_color_max_r = hemi_color_min_r * scale_hemi
	hemi_color_max_g = hemi_color_min_g * scale_hemi
	hemi_color_max_b = hemi_color_min_b * scale_hemi

#Самое темное время
print t_night
night = int(raw_input())
#Самое ясное время
print t_day
day = int(raw_input())

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


#Запись параметров в файл
i1 = 0
step1 = (ambient_max_r - ambient_min_r)/(day - night)
if step1 < 0:
	step1 = step1 * (-1)
print step1
#ИЗМЕНИТЬ ШАГ НА ПРАВИЛЬНЫЙ
step2 = (ambient_max_r - ambient_min_r)/(24 - day - night)
if step2 < 0:
	step2 = step2 * (-1)
print step2

while i1 < 24:
	
	if i1 < 10:
		prefix = '0' + str(i1)
	else:
		prefix = str(i1)

	if (i1 + 1) > night and (i1 + 1) < day:
		ambient_r = str(step1*i1 + ambient_min_r)
		ambient_g = str(step1*i1 + ambient_min_g)
		ambient_b = str(step1*i1 + ambient_min_b)
		hemi_color_r = str(step1*i1 + hemi_color_min_r)
		hemi_color_g = str(step1*i1 + hemi_color_min_g)
		hemi_color_b = str(step1*i1 + hemi_color_min_b)

	else:
		ambient_r = str(ambient_max_r - step2*i1)
		ambient_g = str(ambient_max_g - step2*i1)
		ambient_b = str(ambient_max_b - step2*i1)
		hemi_color_r = str(hemi_color_max_r - step2*i1)
		hemi_color_g = str(hemi_color_max_g - step2*i1)
		hemi_color_b = str(hemi_color_max_b - step2*i1)
		
	
	len_value = 5

	file.write('[' + str(weather_name) + '_' + str(prefix) + ']\n' + 'ambient\t\t\t=\t' + ambient_r[0:len_value] + ',\t' + ambient_g[0:len_value] + ',\t' + ambient_b[0:len_value] + '\nhemi_color\t\t=\t' + hemi_color_r[0:len_value] + ',\t' + hemi_color_g[0:len_value] + ',\t' + hemi_color_b[0:len_value] + '\n'*2)
	i1 += 1

file.close()
raw_input()