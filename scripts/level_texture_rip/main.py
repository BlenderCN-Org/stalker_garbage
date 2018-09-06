import stalker_utils, parse_level, level_prop, time

start_time = time.time()
data = stalker_utils.file_read('level')
file_size = len(data)
position = 0

while position < file_size:
    block_id, block_size, block_data, position = stalker_utils.block_read(data, position)
    if block_id == 0x0002:
        image_list = parse_level.parse_textures(block_data, block_size)
        stalker_utils.copy_files(
        level_prop.texture_path, image_list, level_prop.texture_ext, \
        level_prop.output_dir, level_prop.copy_bump)
finish_time = time.time()
print('total time: {0:.3}s'.format(finish_time-start_time))
input()