import utils, details_prop, details_parse, time

start_time = time.time()

details_data = utils.read_bin_file(details_prop.details_file_name,
                                   details_prop.details_file_ext,
                                   details_prop.details_file_path)
details_parse.details_data_parse(details_data)

finish_time = time.time()
print('total time: {0:.5}s'.format(finish_time - start_time))

try:
    import bpy
    use_blender = True
except:
    use_blender = False

if not use_blender:
    input()