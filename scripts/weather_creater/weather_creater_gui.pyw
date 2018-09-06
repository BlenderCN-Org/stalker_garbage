# Импотируем модуль, который нужен для построения интерфейса.
from tkinter import *

def rgb(red, green, blue):
    """
    Переводит значение цвета к виду '#XXYYZZ'
    Использование: rgb(red, green, blue)
    red, green, blue = (0 - 255) int
    """
    if red < 256 and green < 256 and blue < 256:
        red = str(hex(red))[2:]
        if len(red) < 2:
            red = '0' + red
        green = str(hex(green))[2:]
        if len(green) < 2:
            green = '0' + green
        blue = str(hex(blue))[2:]
        if len(blue) < 2:
            blue = '0' + blue
        return '#' + red + green + blue

def rgb_f(red, green, blue):
    """
    Переводит значение цвета к виду '#XXYYZZ'
    Использование: rgb(red, green, blue)
    red, green, blue = (0.0 - 1.0) float
    """
    if 0.0<=red<=1.0 and 0.0<=green<=1.0 and 0.0<=blue<=1.0:
    
        red = str(hex(int(red*255)))[2:]
        if len(red) < 2:
            red = '0' + red
            
        green = str(hex(int(green*255)))[2:]
        if len(green) < 2:
            green = '0' + green
            
        blue = str(hex(int(blue*255)))[2:]
        if len(blue) < 2:
            blue = '0' + blue
            
        return '#' + red + green + blue

###!!! Строки. Все текстовые строки, которые выводятся в интерфейс.
# Заголовок главного окна.
s_root_wind_title = 'Weather Creater'
# Версия программы, которая отображается в заголовке главного окна.
s_root_wind_version = 'Alpha Version'
# Текст главных меток.
s_label_ambient = 'Ambient'
s_label_hemi_color = 'Hemi Color'
s_label_scale = 'Scale Value'
s_label_day_night = 'Day Cycle'
# Тексты меток в рамках возле полей ввода красного, зелёного, синего цветов.
s_label_red = 'Red'
s_label_green = 'Green'
s_label_blue = 'Blue'
# Минимальное и максимальное значение.
s_label_min = 'Min'
s_label_max = 'Max'
# Самое тёмное и самое светлое время суток.
s_label_svetlo = 'Full Day'
s_label_temno = 'Full Night'
# Кнопка сохранения погоды.
s_button_create_file = 'Create Weather File'
###!!! Строки.

###!!! Цвета, используемые в интерфейсе
# Цвет текста
c_text = rgb_f(0.1, 0.1, 0.1)
# Основной цвет фона рамок
c_frame_bg = rgb_f(0.5, 0.5, 0.5)
# Цвет фона полей ввода
c_entry_background = rgb_f(0.6, 0.6, 0.6)
# Цвет кнопок
c_button_background = rgb_f(0.6, 0.6, 0.6)
###!!! Цвета, используемые в интерфейсе.

###!!! Шрифты
# Шрифт главных меток рамки.
f_label = 'text 12'
# Крупный шрифт меток возле полей со значениями.
f_label_prop_big = 'text 10'
# Мелкий шрифт меток возле полей со значениями.
f_label_prop_small = 'text 8'
###!!! Шрифты

###!!! Параметры расположения виджетов.
# Размер бардюра в рамках.
border_size = 8
# Ширина поля ввода.
entry_width = 10
# Бардюр поля ввода.
entry_border = 1
# Расстояние по горизонтали от меток до других виджетов.
label_grid_padx = 2
###!!! Параметры расположения виджетов.

# Главное окно.
# Переменной root назначаем главное окно программы из импортированного модуля.
root = Tk()
# Минимальный размер главного окна.
root.minsize(width = 550, height = 311)
# Максимальный размер главного окна.
root.maxsize(width = 550, height = 311)
# нельзя менять размер окна
root.resizable(height = False, width = False)
# Добавляем атрибут "заголовок" главному окну.
root.title(string = '   ..:: ' + s_root_wind_title + ' ::..   ' + s_root_wind_version)
# иконка в заголовке
root.iconbitmap(bitmap = 'wc.ico')
# Главная рамка.
# Главная рамка, на которой распологаются все остальные рамки.
root_frame = Frame(root, width = 0, height = 0, bg = c_frame_bg, bd = border_size)
# Размещаем главную рамку на окне root.
root_frame.grid(row = 0, column = 0)

def create_frame_property(frame_row, frame_column, s_lebel):
	# Добавляет рамку, в которой содержатся параметры для настройки погоды.
	frame_property = Frame(root_frame, width = 320, height = 160, bg = c_frame_bg, bd = border_size)
	# Распологает на главном окне рамку.
	frame_property.grid(row = frame_row, column = frame_column)
	###!!! МЕТКИ
	# Создаём метку в рамке.
	label_frame_title = Label(
	frame_property, text = s_lebel, font = f_label, 
	background = c_frame_bg, foreground = c_text
	)
	# Распологаем метку методом pack().
	label_frame_title.grid(
	row = 0, column = 2, padx = label_grid_padx
	)
	# Метка возле поля ввода красного цвета параметра.
	label_red = Label(
	frame_property, text = s_label_red, 
	font = f_label_prop_small, background = c_frame_bg
	)
	# Распологаем метку label_red
	label_red.grid(
	row = 1, column = 1, padx = label_grid_padx
	)
	# Остальные рамки ввода других цветов.
	label_green = Label(
	frame_property, text = s_label_green, font = f_label_prop_small,
	background = c_frame_bg
	)
	label_green.grid(
	row = 1, column = 2, padx = label_grid_padx
	)
	label_blue = Label(
	frame_property, text = s_label_blue, font = f_label_prop_small, 
	background = c_frame_bg
	)
	label_blue.grid(
	row = 1, column = 3, padx = label_grid_padx
	)
	# Метки минимума и максимума.
	label_min = Label(
	frame_property, text = s_label_min, font = f_label_prop_big, 
	background = c_frame_bg
	)
	label_min.grid(
	row = 2, column = 0, padx = label_grid_padx
	)
	label_max = Label(
	frame_property, text = s_label_max, font = f_label_prop_big, 
	background = c_frame_bg
	)
	label_max.grid(
	row = 3, column = 0, padx = label_grid_padx
	)
	###!!! ПОЛЯ ВВОДА
	# Min
	entry_red_min = Entry(
	frame_property, width = entry_width, bd = entry_border, 
	background = c_entry_background
	)
	entry_red_min.grid(
	row = 2, column = 1, padx = label_grid_padx
	)
	# Минимальный красный
	red_min = entry_red_min.get()
	entry_green_min = Entry(
	frame_property, width = entry_width, bd = entry_border, 
	background = c_entry_background
	)
	entry_green_min.grid(
	row = 2, column = 2, padx = 5
	)
	# Минимальный зелёный.
	green_min = entry_green_min.get()
	entry_blue_min = Entry(
	frame_property, width = entry_width, bd = entry_border, 
	background = c_entry_background
	)
	entry_blue_min.grid(
	row = 2, column = 3, padx = label_grid_padx
	)
	# Минимальный синий.
	blue_min = entry_blue_min.get()
	# Max
	entry_red_max = Entry(
	frame_property, width = entry_width, bd = entry_border, 
	background = c_entry_background
	)
	entry_red_max.grid(row = 3, column = 1, padx = label_grid_padx
	)
	# Максимальный красный.
	red_max = entry_red_max.get()
	entry_green_max = Entry(
	frame_property, width = entry_width, bd = entry_border, 
	background = c_entry_background
	)
	entry_green_max.grid(
	row = 3, column = 2, padx = label_grid_padx
	)
	# Максимальный зелёный.
	green_max = entry_green_max.get()
	entry_blue_max = Entry(
	frame_property, width = entry_width, bd = entry_border, 
	background = c_entry_background
	)
	entry_blue_max.grid(
	row = 3, column = 3, padx = label_grid_padx
	)
	# Максимальный синий.
	blue_max = entry_blue_max.get()
	return red_min, green_min, blue_min, red_max, green_max, blue_max

def frame_property_2(frame_row, frame_column, s_lebel, s_label_1, s_label_2):
	# Рамки масштабирования параметров и рамка времени суток.
	frame_property = Frame(root_frame, width = 320, height = 160, bg = c_frame_bg, bd = border_size)
	frame_property.grid(row = frame_row, column = frame_column)
	
	label_frame_title = Label(
	frame_property, text = s_lebel, font = f_label, 
	background = c_frame_bg, foreground = c_text
	)
	label_frame_title.grid(
	row = 0, column = 1, padx = label_grid_padx
	)
	label_1 = Label(
	frame_property, text = s_label_1, font = f_label_prop_big, 
	background = c_frame_bg
	)
	label_1.grid(
	row = 1, column = 0, padx = label_grid_padx
	)
	label_2 = Label(
	frame_property, text = s_label_2, font = f_label_prop_big, 
	background = c_frame_bg
	)
	label_2.grid(
	row = 2, column = 0, padx = label_grid_padx
	)
	entry_value_1 = Entry(
	frame_property, width = entry_width, bd = entry_border, 
	background = c_entry_background
	)
	entry_value_1.grid(
	row = 1, column = 1, padx = label_grid_padx
	)
	entry_value_2 = Entry(
	frame_property, width = entry_width, bd = entry_border, 
	background = c_entry_background
	)
	entry_value_2.grid(
	row = 2, column = 1, padx = label_grid_padx
	)


button_save_file = Button(
root_frame, text = s_button_create_file, width = 19, height = 1, bg = c_button_background, 
fg = c_text, activebackground = c_frame_bg
)

button_save_file.grid(row = 3, column = 0)

frame_property_2(1, 0, s_label_scale, s_label_ambient, s_label_hemi_color)
frame_property_2(1, 1, s_label_day_night, s_label_svetlo, s_label_temno)
frame_property_2(2, 0, 'Names', 'Save File', 'Weather Sect')
create_frame_property(0, 0, s_label_ambient)
create_frame_property(0, 1, s_label_hemi_color)
root.mainloop()		# Запускаем главное окно root.