import read_file, ogf_prop, ogf_parse, time

start_time = time.time()

ogf_data = read_file.read_file(ogf_prop.ogf_file_path, ogf_prop.ogf_file_name, ogf_prop.ogf_file_ext)
ogf_parse.ogf_data_parse(ogf_data)

finish_time = time.time()
print(finish_time - start_time)

try:
    import bpy
    use_blender = True
except:
    use_blender = False

if not use_blender:
    input()