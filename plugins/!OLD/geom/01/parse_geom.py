from struct import unpack

f = open(r'c:\level.geom', 'rb')
s = f.read()
f.close()

save = open(r'1.txt', 'w')

try:
    import bpy
    useBlender = True
except:
    useBlender = False

p = 0

while p < len(s):
    print('='*79)
    block_id, compress, block_size = unpack('2hi', s[p : p + 8])
    p += 8
    print('Номер блока {}\nСжатие данных {}\nРазмер блока {}'.format(block_id, compress, block_size))
    
    if block_id == 1:   # Версия компилятора карты
        version = unpack('h', s[p : p + 2])[0]   #Номер версии (для всех одинаковый)
        p += 2
        unknow = list(map(hex, unpack('2b', s[p : p + 2])))
        p += 2
        print('\tБлок версии компилятора\n\tНомер версии', version)
        print('\tНеизвестные данные', unknow[0], unknow[1])
    
    elif block_id == 9:     # Описание вершин
        vertex_block_count = unpack('i', s[p : p + 4])[0]    # Количество блоков описания вершин
        p += 4
        print('\tБлок описания вершин\n\tКоличество блоков вершин', vertex_block_count)
        
        for i in range(vertex_block_count):
            
            start_new_block = unpack('i', s[p : p + 4])[0]    # Начало нового блока
            p += 4
            print('\tНачало нового блока', start_new_block)
            
            start_format_vertex = unpack('i', s[p : p + 4])[0]  # Начало описания формата вершины
            p += 4
            print('\tНачало описания формата вершины', start_format_vertex)
            
            vertex_format = unpack('4h', s[p : p + 8])
            p += 8
            
            unknow = s[p : p + 32]
            p += 32
            print('\tunknow (32 bytes)')
            
            print('\tФормат вершин' \
            '\n\t\tВсегда ноль {0}\n\t\tСмещение {1}\n\t\tТип переменных {2}\n\t\t' \
            'Что описывают переменные {3}'.format(
            vertex_format[0], vertex_format[1], vertex_format[2], vertex_format[3]))
            
            end_format_vertex = unpack('i', s[p : p + 4])[0]    # Конец описания формата вершины
            p += 4
            print('\tКонец описания формата вершины', end_format_vertex)
            
            start_vertex = unpack('i', s[p : p + 4])[0]    # Начало описания вершин
            p += 4
            print('\tНачало описания вершин', start_vertex)
            
            vertex_count = unpack('i', s[p : p + 4])[0]
            p += 4
            print('\tКоличество вершин', vertex_count)
            
            vertices = []
            uvs = []
            
            for i in range(vertex_count):
                coord = unpack('3f', s[p : p + 12])
                print(coord)
                print(i + 1, coord, file = save)
                p += 12
                
                vertices.append(coord)
                
                normal = unpack('3b', s[p : p + 3])
                # print(normal)
                p += 3
                
                light_factor = unpack('b', s[p : p + 1])[0]
                # print(light_factor)
                p += 1
                
                tangent = unpack('3b', s[p : p + 3])
                # print(tangent)
                p += 3
                
                corector_uv_x = unpack('b', s[p : p + 1])[0]
                # print(corector_uv_x)
                p += 1
                
                bi_tangent = unpack('3b', s[p : p + 3])
                # print(bi_tangent)
                p += 3
                
                corector_uv_y = unpack('b', s[p : p + 1])[0]
                # print(corector_uv_y)
                p += 1
                
                uv = unpack('2f', s[p : p + 8])
                # print(uv)
                p += 8
                
                uvs.append(uv)
                
                #uv_lmap = unpack('2h', s[p : p + 4])
                #print(uv_lmap)
                #p += 4
    
    elif block_id == 10:     # Описание индексов
        index_block_count = unpack('i', s[p : p + 4])[0]    # Количество блоков описания индексов
        p += 4
        print('\tКоличество блоков индексов', index_block_count)
        
        faces = []
        
        for i in range(index_block_count):
            index_count = unpack('i', s[p : p + 4])[0]
            p += 4
            print('\tКоличество индексов в блоке', index_count)
            
            for i in range(index_count//3):
                i1, i2, i3 = unpack('3h', s[p : p + 6])
                faces.append([i1, i2, i3])
                p += 6
                print(i1 + 1, i2 + 1, i3 + 1, file = save)

            
            '''
            indices = unpack('%dh' % index_count, s[p : p + (index_count*2)])
            p += index_count * 2'''
    
    elif block_id == 11:
        unknow = unpack('4b', s[p : p + 4])
        p += 4
        print('\tБлок синхронизации (?)\n\tНеизвестные данные', list(map(hex, unknow)))
    
    else:
        p += block_size

print('='*79)

save.close()

if useBlender:
    mesh = bpy.data.meshes.new('GEOM')
    object = bpy.data.objects.new('GEOM', mesh)
    scene = bpy.context.scene
    scene.objects.link(object)
    mesh.from_pydata(vertices,(),faces)
    
else:
    input('finish')
    