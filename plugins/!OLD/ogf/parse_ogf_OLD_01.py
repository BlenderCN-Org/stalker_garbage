from struct import unpack
import datetime

file = open('1.ogf', 'rb')
s = file.read()
file.close()

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
        print(hex(block_id), end = ' ')
        print(block_size)
        p += block_size
        
    
input()