import utils, hom_prop, hom_parse, time

start_time = time.time()

hom_data = utils.read_bin_file(hom_prop.hom_file_name,
                               hom_prop.hom_file_ext,
                               hom_prop.hom_file_path)

hom_parse.hom_data_parse(hom_data, hom_prop.hom_file_name+'_'+hom_prop.hom_file_ext)

finish_time = time.time()
print('total time: {0:.5}s'.format(finish_time - start_time))

try:
    import bpy
    use_blender = True
except:
    use_blender = False

if not use_blender:
    input()