import stalker_utils, struct, parse_data, import_mesh

data = stalker_utils.file_read('c:\\level')
file_size = len(data)
position = 0
#save = open('save.bin', 'wb')
while position < file_size:
    block_id, block_size, block_data, position = stalker_utils.block_read(data, position)
    if block_id == 0x1:
        pass
        # parse_data.parse_header(block_data)
    elif block_id == 0x02:
        pass
        # parse_data.parse_shaders(block_data)
    elif block_id == 0x04:
        vertices = parse_data.parse_vertices(block_data)
        import_mesh.crete_mesh(vertices)
        #save.write(block_data)
        #save.close()
    else:
        print(hex(block_id), block_size)
try:
    import bpy
except:
    input()