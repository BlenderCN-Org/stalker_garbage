import struct

def u(s, r, o = 'out_integer'):        # unpack
    """
    Распаковывает данные.
    
    Использование:
    u(s, r, o)
    
    s - строка, которую нужно распаковать
    r - режим функции struct.unpack ('i', '3f', 'f', 'ifi' ...)
    o - режим вывода
        out_integer - число
        out_hex - hex(число)
        out_tuple - кортеж (число1, число2, число3 ...)
        out_block_size - (p+=block_size)
    """
    
    
    global p
    size = struct.calcsize(r)
    if (p + size) > len(s):
        return None
    unpack_data = struct.unpack(r, s[p : p + size])
    
    if o == 'out_integer':    # default, для распаковки одного числа
        p += size
        return unpack_data[0]
    elif  o == 'out_hex':    # hex, для распаковки идентификатора блока
        p += size
        if p > len(s):
            run = False
        return hex(unpack_data[0])
    elif o == 'out_tuple':    # tuple, для распаковки кортежа, содержащего несколько чисел
        p += size
        return unpack_data
    elif o == 'out_block_size':
        p += size
        p += unpack_data[0]
        return unpack_data[0]
    else:
        pass

# часто используемые переменные
o1 = 'out_integer'        # Default (integer)
o2 = 'out_hex'            # HEX
o3 = 'out_tuple'        # Tuple
o4 = 'out_block_size'    # block size (int)
p = 0        # положение считывания из файла s