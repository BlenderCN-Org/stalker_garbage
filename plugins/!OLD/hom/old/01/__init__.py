import read_file, hom_prop, hom_parse, time

start_time = time.time()

hom_data = read_file.read_file(hom_prop.hom_file_path, hom_prop.hom_file_name, hom_prop.hom_file_ext)
hom_parse.hom_data_parse(hom_data, hom_prop.hom_file_name+'_'+hom_prop.hom_file_ext)

finish_time = time.time()
print(finish_time - start_time)

try:
    import bpy
    use_blender = True
except:
    use_blender = False

if not use_blender:
    input()