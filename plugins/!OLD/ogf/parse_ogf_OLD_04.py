from struct import unpack
import datetime

file = open(r'ogf2.ogf', 'rb')
s = file.read()
file.close()

save = open('save.txt', 'w')

def parse_child(s):
    p = 0
    
    while p < len(s):
            
        block_id = unpack('i', s[p : p + 4])[0]
        p += 4
        
        block_size = unpack('i', s[p : p + 4])[0]
        p += 4
        
        if block_id == 0x1:
            print('Header', hex(block_id))
            
            format_version = unpack('b', s[p : p + 1])[0]
            p += 1
            print('\tVersion =', format_version)
            
            type = unpack('b', s[p : p + 1])[0]
            p += 1
            print('\tType: ', type)
            
            shader_id = unpack('h', s[p : p + 2])[0]
            p += 2
            print('\tShader ID =', shader_id)
            
            bbox = unpack('6f', s[p : p + 24])
            p += 24
            print('\tBounding Box:', '\t', bbox[:3], '\n\t\t\t\t\t', bbox[3:])
            
            sphere_center = unpack('3f', s[p : p + 12])
            p += 12
            print('\tSphere Center:', sphere_center)
            
            sphere_radius = unpack('f', s[p : p + 4])[0]
            p += 4
            print('\tSphere Radius:', sphere_radius)
        
        elif block_id == 0x2:
            print('Texture', hex(block_id))
            
            texture_name = ''
            ch = unpack('s', s[p : p + 1])[0]
            p += 1
            while ch != b'\x00':
                texture_name += str(ch)[2:-1]
                ch = unpack('s', s[p : p + 1])[0]
                p += 1
            
            shader_name = ''
            ch = unpack('s', s[p : p + 1])[0]
            p += 1
            while ch != b'\x00':
                shader_name += str(ch)[2:-1]
                ch = unpack('s', s[p : p + 1])[0]
                p += 1
            
            print('\tTexture: {}, Shader: {}'.format(texture_name, shader_name))
            
        elif block_id == 0x3:
            ogf_vertexformat_fvf_1l = 0x12071980
            ogf_vertexformat_fvf_2l = 0x240e3300
            ogf_vertexformat_fvf_old = 0x00000112  # ДОРАБОТАТЬ ЭТОТ ФОРМАТ
            
            print('Vertex', hex(block_id))
            
            vertex_format, vertex_count = unpack('2i', s[p : p + 8])
            p += 8
            print('\tVertex Format {}, Vertex Count {}'.format(hex(vertex_format), vertex_count))
            
            if vertex_format == ogf_vertexformat_fvf_1l or vertex_format == 1:
                for i in range(vertex_count):
                    mesh_data = unpack('14fi', s[p : p + 60])
                    p += 60
                    
                    # print('\nvertex%d' % i)
                    
                    point = mesh_data[0:3]
                    normal = mesh_data[3:6]
                    t = mesh_data[6:9]
                    b = mesh_data[9:12]
                    u, v = mesh_data[12:14]
                    matrix = mesh_data[14]
                    
                    # print('point:', point)
                    # print('normal:', normal)
                    # print('matrix:', matrix)
                    # print('t:', t)
                    # print('b:', b)
                    # print('u, v:', (u, v))
            
            elif vertex_format == ogf_vertexformat_fvf_2l or vertex_format == 2:
                
                for i in range(vertex_count):
                    mesh_data = unpack('2h15f', s[p : p + 64])
                    p += 64
                    
                    # print('\nvertex%d' % i)
                    
                    matrix0 = mesh_data[0]
                    matrix1 = mesh_data[1]
                    point = mesh_data[2:5]
                    normal = mesh_data[5:8]
                    t = mesh_data[8:11]
                    b = mesh_data[11:14]
                    w = mesh_data[14]
                    u, v = mesh_data[15:17]
                    
                    # print('matrix0:', matrix0)
                    # print('matrix1:', matrix1)
                    # print('point:', point)
                    # print('normal:', normal)
                    # print('t:', t)
                    # print('b:', b)
                    # print('w:', w)
                    # print('u, v:', (u, v))
        
            elif vertex_format == ogf_vertexformat_fvf_old:
                for i in range(vertex_count):
                    mesh_data = unpack('8f', s[p : p + 32])
                    p += 32
                    
                    print('\nvertex%d' % i)
                    
                    point = mesh_data[0:3]
                    normal = mesh_data[3:6]
                    u, v = mesh_data[6:8]
                    
                    print('point:', point)
                    print('normal:', normal)
                    print('u, v:', (u, v))
            '''
            else:
                p -= 8 # vertex_format and vertex_count (2i -> 8 bytes)
                print('\n\nVERTEX FORMAT = UNKNOW')
                p += block_size
                '''
                
        elif block_id == 0x4:
            print('Indices', hex(block_id))
            
            indices_count = unpack('i', s[p : p + 4])[0]
            p += 4
            print('Indices Count =', indices_count)
            
            for i in range(indices_count):
                index = unpack('h', s[p : p + 2])[0]
                p += 2
                print('\tIndex =', index)
        
        elif block_id == 0x6:
            print('Swidata', hex(block_id))
            
            reserved = unpack('4i', s[p : p + 16])
            p += 16
            print('Reverved =', reserved)
            
            count = unpack('i', s[p : p + 4])[0]
            p += 4
            print('Count =', count)
            
            for i in range(count):
                data0 = unpack('i', s[p : p + 4])[0]
                p += 4
                data1 = unpack('2h', s[p : p + 4])
                p += 4
                
                # print('slide_window', i, sep = '')
                # print('\toffset:', hex(data0))
                # print('\tnum_tris:', data1[0])
                # print('\tnum_verts:', data1[1])
        
        else:
            print('!!!', hex(block_id), ' = ', block_size)
            p += block_size

def parse_mesh(s):
    p = 0
    
    while p < len(s):
        child = unpack('i', s[p : p + 4])[0]
        p += 4
        
        child_size = unpack('i', s[p : p + 4])[0]
        p += 4
        
        print('Child:', child)
        
        parse_child(s[p : p + child_size])
        
        p += child_size

def parse_motion(s):
    print('\tSM Params:')
    p = 0
    version = unpack('h', s[p : p + 2])[0]
    p += 2
    print('\tVersion', version)
    
    partition_count = unpack('h', s[p : p + 2])[0]
    p += 2
    print('\tPartition Count', partition_count)
    
    for i in range(partition_count):
        partition_name = ''
        ch = ''
        while ch != b'\x00':
            ch = unpack('s', s[p : p + 1])[0]
            p += 1
            partition_name += str(ch)[2:-1]
        print('\tPartition Name:', partition_name[:-4])
        
        bone_count = unpack('h', s[p : p + 2])[0]
        p += 2
        print('\n\tBone Count =', bone_count)
        
        for i in range(bone_count):
            bone_name = ''
            ch = ''
            while ch != b'\x00':
                ch = unpack('s', s[p : p + 1])[0]
                p += 1
                bone_name += str(ch)[2:-1]
            bone_id = unpack('i', s[p : p + 4])[0]
            p += 4
            print('\t{0:0>2}'.format(bone_id), bone_name[:-4])
            
        motion_count = unpack('h', s[p : p + 2])[0]
        p += 2
        print('\n\tMotion Count = %d\n' % motion_count)
        
        for i in range(motion_count):
            motion_name = ''
            ch = ''
            while ch != b'\x00':
                ch = unpack('s', s[p : p + 1])[0]
                p += 1
                motion_name += str(ch)[2:-1]
            print('\tMotion Name:', motion_name[:-4])
            
            flags = unpack('i', s[p : p + 4])[0]
            p += 4
            print('\tFlags =', flags)
            
            bone_part = unpack('h', s[p : p + 2])[0]
            p += 2
            if bone_part == -1:
                print('\tBone Part: --all bones--')
            else:
                print('\tBone Part Number =', bone_part)
            
            motion = unpack('h', s[p : p + 2])[0]
            p += 2
            print('\tMotion =', motion)
            
            speed = unpack('f', s[p : p + 4])[0]
            p += 4
            print('\tSpeed = %.2f' % speed)
            
            power = unpack('f', s[p : p + 4])[0]
            p += 4
            print('\tPower = %.2f' % power)
            
            accrue = unpack('f', s[p : p + 4])[0]
            p += 4
            print('\tAccrue = %.2f' % accrue)
            
            falloff = unpack('f', s[p : p + 4])[0]
            p += 4
            print('\tFalloff = %.2f\n' % falloff)

def parse_ikdata(s):
    print('Block 0x10:\n')
    
    p = 0
    
    while p < len(s):
        unknow = str(s[p : p + 4])[2:-1]
        p += 4
        print('Unkow:', unknow)
        
        game_mtl_name = ''
        ch = unpack('s', s[p : p + 1])[0]
        p += 1
        while ch != b'\x00':
            game_mtl_name += str(ch)[2:-1]
            ch = unpack('s', s[p : p + 1])[0]
            p += 1
        print('Geme Material Name:', game_mtl_name)
        
        type = unpack('h', s[p : p + 2])[0]
        p += 2
        print('Type:', type)
        
        flags = unpack('h', s[p : p + 2])[0]
        p += 2
        print('Flags:', flags)
        
        # BOX
        box_rotate = unpack('9f', s[p : p + 36])
        p += 36
        print('\n\tRotate:')
        
        print('\t%.6f %.6f %.6f' % (box_rotate[0], box_rotate[1], box_rotate[2]))
        print('\t%.6f %.6f %.6f' % (box_rotate[3], box_rotate[4], box_rotate[5]))
        print('\t%.6f %.6f %.6f' % (box_rotate[6], box_rotate[7], box_rotate[8]))
        
        box_translate = unpack('3f', s[p : p + 12])
        p += 12
        print('\n\ttranslate:\n\t%.6f %.6f %.6f' % (box_translate[0], box_translate[1], box_translate[2]))
        
        box_halfsize = unpack('3f', s[p : p + 12])
        p += 12
        print('\n\thalfsize:\n\t%.6f %.6f %.6f' % (box_halfsize[0], box_halfsize[1], box_halfsize[2]))
        
        # SPHERE
        sphere_center = unpack('3f', s[p : p + 12])
        p += 12
        print('Sphere Center:', sphere_center)
        
        sphere_radius = unpack('f', s[p : p + 4])[0]
        p += 4
        print('Sphere Radius =', sphere_radius)
        
        # CYLINDER
        
        cylinder_center = unpack('3f', s[p : p + 12])
        p += 12
        
        cylinder_direction = unpack('3f', s[p : p + 12])
        p += 12
        
        cylinder_height = unpack('f', s[p : p + 4])[0]
        p += 4
        
        cylinder_radius = unpack('f', s[p : p + 4])[0]
        p += 4
        
        type = unpack('i', s[p : p + 4])[0]
        p += 4
        print('Type:', type)
        
        for i in range(0, 3):
            print('Limit%d' % i)
            
            limit_range = unpack('2f', s[p : p + 8])
            p += 8
            print('\tRange:', limit_range)
            
            spring_factor = unpack('f', s[p : p + 4])[0]
            p += 4
            print('Spring Factor =', spring_factor)
            
            damping_factor = unpack('f', s[p : p + 4])[0]
            p += 4
            print('Damping Factor =', damping_factor)

        spring_factor = unpack('f', s[p : p + 4])[0]
        p += 4
        print('Spring Factor =', spring_factor)
        
        damping_factor = unpack('f', s[p : p + 4])[0]
        p += 4
        print('Damping Factor =', damping_factor)
        
        ik_flags = unpack('i', s[p : p + 4])[0]
        p += 4
        print('IK Flags:', ik_flags)
        
        break_force = unpack('f', s[p : p + 4])[0]
        p += 4
        print('Break Force =', break_force)
        
        break_torque = unpack('f', s[p : p + 4])[0]
        p += 4
        print('Break Torque =', break_torque)
        
        
        friction = unpack('f', s[p : p + 4])[0]
        p += 4
        print('Friction =', friction)
        
        bind_rotation = unpack('3f', s[p : p + 12])
        p += 12
        print('Bind Rotation:', bind_rotation)
        
        bind_position = unpack('3f', s[p : p + 12])
        p += 12
        print('Bind Position:', bind_position)
        
        mass = unpack('f', s[p : p + 4])[0]
        p += 4
        print('Mass =', mass)
        
        center_of_mass = unpack('3f', s[p : p + 12])
        p += 12
        print('Center Of Mass =', center_of_mass)
        
p = 0

while p < len(s):
    block_id = unpack('i', s[p : p + 4])[0]
    p += 4
    
    block_size = unpack('i', s[p : p + 4])[0]
    p += 4
    
    if block_id == 0x1:
        print('Block 0x1:\n')
        format_version = unpack('b', s[p : p + 1])[0]
        print('\tVersion OGF', format_version)
        p += 1
        
        mesh_type = unpack('b', s[p : p + 1])[0]
        p += 1
        
        if mesh_type == 0:
            print('\tMesh Type - NORMAL')
        elif mesh_type == 1:
            print('\tMesh Type - HIERRARHY')
        elif mesh_type == 2:
            print('\tMesh Type - PROGRESSIVE')
        elif mesh_type == 3:
            print('\tMesh Type - SKELETON_ANIM')
        elif mesh_type == 4:
            print('\tMesh Type - SKELETON_GEOMDEF_PM')
        elif mesh_type == 5:
            print('\tMesh Type - SKELETON_GEOMDEF_ST')
        elif mesh_type == 6:
            print('\tMesh Type - LOD')
        elif mesh_type == 7:
            print('\tMesh Type - TREE_ST')
        elif mesh_type == 8:
            print('\tMesh Type - PARTICLE_EFFECT')
        elif mesh_type == 9:
            print('\tMesh Type - PARTICLE_GROUP')
        elif mesh_type == 10:
            print('\tMesh Type - SKELETON_RIGID')
        elif mesh_type == 11:
            print('\tMesh Type - TREE_PM')
        else:
            print('\tMesh Type - <UNKNOW>')
        
        shader_id = unpack('h', s[p : p + 2])[0]
        p +=2
        print('\tShader ID =', shader_id)
        
        bbox = unpack('6f', s[p : p + 24])
        p += 24
        print('\n\tBounding Box:\n\t\tMin:\t', end = '')
        
        for i in bbox[:3]:
            print(round(i, 2), end = '\t')
        
        print('\n\t\tMax:\t', end = '')
        
        for i in bbox[3:]:
            print(round(i, 2), end = '\t')
        
        print()
        
        bsphere = unpack('4f', s[p : p + 16])
        p += 16
        print('\n\tBSphere:\n\t\tCenter:\t', end = '')
        for i in bsphere[:3]:
            print(round(i, 4), end = '\t')
            
        print('\n\t\tRadius:', end = '')
        print('\t', round(bsphere[3], 4))
    
    elif block_id == 0x2:
        print('Texture', hex(block_id))
            
        texture_name = ''
        ch = unpack('s', s[p : p + 1])[0]
        p += 1
        while ch != b'\x00':
            texture_name += str(ch)[2:-1]
            ch = unpack('s', s[p : p + 1])[0]
            p += 1
        
        shader_name = ''
        ch = unpack('s', s[p : p + 1])[0]
        p += 1
        while ch != b'\x00':
            shader_name += str(ch)[2:-1]
            ch = unpack('s', s[p : p + 1])[0]
            p += 1
        
        print('\tTexture: {}, Shader: {}'.format(texture_name, shader_name))
    
    elif block_id == 0x3:
        ogf_vertexformat_fvf_1l = 0x12071980
        ogf_vertexformat_fvf_2l = 0x240e3300
        ogf_vertexformat_fvf_old = 0x00000112  # ДОРАБОТАТЬ ЭТОТ ФОРМАТ
            
        print('Vertex', hex(block_id))
        
        vertex_format, vertex_count = unpack('2i', s[p : p + 8])
        p += 8
        print('\tVertex Format {}, Vertex Count {}'.format(hex(vertex_format), vertex_count))
        
        if vertex_format == ogf_vertexformat_fvf_1l or vertex_format == 1:
            for i in range(vertex_count):
                mesh_data = unpack('14fi', s[p : p + 60])
                p += 60
                
                # print('\nvertex%d' % i)
                
                point = mesh_data[0:3]
                normal = mesh_data[3:6]
                t = mesh_data[6:9]
                b = mesh_data[9:12]
                u, v = mesh_data[12:14]
                matrix = mesh_data[14]
                
                # print('point:', point)
                # print('normal:', normal)
                # print('matrix:', matrix)
                # print('t:', t)
                # print('b:', b)
                # print('u, v:', (u, v))
        
        elif vertex_format == ogf_vertexformat_fvf_2l or vertex_format == 2:
            
            for i in range(vertex_count):
                mesh_data = unpack('2h15f', s[p : p + 64])
                p += 64
                
                # print('\nvertex%d' % i)
                
                matrix0 = mesh_data[0]
                matrix1 = mesh_data[1]
                point = mesh_data[2:5]
                normal = mesh_data[5:8]
                t = mesh_data[8:11]
                b = mesh_data[11:14]
                w = mesh_data[14]
                u, v = mesh_data[15:17]
                
                # print('matrix0:', matrix0)
                # print('matrix1:', matrix1)
                # print('point:', point)
                # print('normal:', normal)
                # print('t:', t)
                # print('b:', b)
                # print('w:', w)
                # print('u, v:', (u, v))
        elif vertex_format == ogf_vertexformat_fvf_old:
            for i in range(vertex_count):
                mesh_data = unpack('8f', s[p : p + 32])
                p += 32
                
                print('\nvertex%d' % i)
                
                point = mesh_data[0:3]
                normal = mesh_data[3:6]
                u, v = mesh_data[6:8]
                
                print('point:', point)
                print('normal:', normal)
                print('u, v:', (u, v))
            
        else:
            p -= 8 # vertex_format and vertex_count (2i -> 8 bytes)
            print('\n\nVERTEX FORMAT = UNKNOW')
            p += block_size
    
    elif block_id == 0x4:
        print('Indices', hex(block_id))
        
        indices_count = unpack('i', s[p : p + 4])[0]
        p += 4
        print('Indices Count =', indices_count)
        
        for i in range(indices_count):
            index = unpack('h', s[p : p + 2])[0]
            p += 2
            print('\tIndex =', index)
    
    elif block_id == 0x09:
        print('Block 0x09:\n')
        parse_mesh(s[p : p + block_size])
        p += block_size
    
    elif block_id == 0x10:
        parse_ikdata(s[p : p + block_size])
        print(block_size)
        p += block_size
    
    elif block_id == 0x11:
        print('Block 0x11:\n')
        user_data = str(s[p : p + block_size - 1])[2:-1]
        print('\tUser Data:\n\t', user_data, sep = '')
        p += block_size
    
    elif block_id == 0x12:
        print('Block 0x12:\n')
        sourse_path = ''
        ch = ''
        while ch != b'\x00':
            ch = unpack('s', s[p : p + 1])[0]
            p += 1
            sourse_path += str(ch)[2:-1]
        
        print('\tSourse Path:\t', sourse_path[:-4])
        
        ogf_creator = ''
        ch = ''
        while ch != b'\x00':
            ch = unpack('s', s[p : p + 1])[0]
            p += 1
            ogf_creator += str(ch)[2:-1]
        
        print('\tOGF Creator:\t', ogf_creator[:-4])
        
        unknow = s[p : p + 4]
        p += 4
        print('\tUNKNOW DATA:\t', str(unknow)[2:-1])
        
        creator = ''
        ch = ''
        while ch != b'\x00':
            ch = unpack('s', s[p : p + 1])[0]
            p += 1
            creator += str(ch)[2:-1]
        print('\tCreator:\t', creator[:-4])
        
        create_time = unpack('i', s[p : p + 4])[0]
        p += 4
        print('\tCreate Time:\t', create_time)
        
        editor = ''
        ch = ''
        while ch != b'\x00':
            ch = unpack('s', s[p : p + 1])[0]
            p += 1
            editor += str(ch)[2:-1]
        print('\tEditor:\t\t', editor[:-4])
        
        edit_time = unpack('i', s[p : p + 4])[0]
        p += 4
        print('\tEdit Time:\t', edit_time)
        
    elif block_id == 0xd:
        print('Block 0xd:\n')
        
        bone_count = unpack('i', s[p : p + 4])[0]
        p += 4
        print('\n\tBone Count =', bone_count)
        
        for i in range(bone_count):
            print('\n\tbone%.2i :' % (i + 1))
            bone_name = ''
            ch = unpack('s', s[p : p + 1])[0]
            p += 1
            while ch != b'\x00':
                bone_name += str(ch)[2:-1]
                ch = unpack('s', s[p : p + 1])[0]
                p += 1
            print('\n\tBone Name:', bone_name)
            
            parent_name = ''
            ch = unpack('s', s[p : p + 1])[0]
            p += 1
            while ch != b'\x00':
                parent_name += str(ch)[2:-1]
                ch = unpack('s', s[p : p + 1])[0]
                p += 1
            print('\n\tParent Bone Name:', parent_name)
            
            bone_rotate = unpack('9f', s[p : p + 36])
            p += 36
            print('\n\tRotate:')
            
            print('\t%.6f %.6f %.6f' % (bone_rotate[0], bone_rotate[1], bone_rotate[2]))
            print('\t%.6f %.6f %.6f' % (bone_rotate[3], bone_rotate[4], bone_rotate[5]))
            print('\t%.6f %.6f %.6f' % (bone_rotate[6], bone_rotate[7], bone_rotate[8]))
            
            bone_translate = unpack('3f', s[p : p + 12])
            p += 12
            print('\n\ttranslate:\n\t%.6f %.6f %.6f' % (bone_translate[0], bone_translate[1], bone_translate[2]))
            
            bone_halfsize = unpack('3f', s[p : p + 12])
            p += 12
            print('\n\thalfsize:\n\t%.6f %.6f %.6f' % (bone_halfsize[0], bone_halfsize[1], bone_halfsize[2]))

            
        
    elif block_id == 0x0f:
        print('Block 0x0f:\n')
        parse_motion(s[p : p + block_size])
        p += block_size
        
    else:
        print('Осталось разобрать:')
        print(hex(block_id), block_size)
        p += block_size
save.close()
input()