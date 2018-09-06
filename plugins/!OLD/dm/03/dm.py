import time, utils, import_utils, dm_parse

start_time = time.time()

dm_file_path = 'c:\\'
dm_file_name = 'rain'
dm_file_ext = 'dm'
dm_data = utils.read_bin_file(dm_file_name, dm_file_ext, dm_file_path)
vertices, uvs, triangles, texture_name = dm_parse.parse_main(dm_data)
import_utils.crete_mesh(vertices, triangles, uvs=uvs, image=texture_name)

finish_time = time.time()
print('total time: {}s'.format(finish_time - start_time))