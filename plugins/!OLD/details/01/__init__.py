import read_file, details_prop, details_parse, time

start_time = time.time()

details_data = read_file.read_file(details_prop.details_file_path, details_prop.details_file_name, details_prop.details_file_ext)
details_parse.details_data_parse(details_data)

finish_time = time.time()
print(finish_time - start_time)

try:
    import bpy
    use_blender = True
except:
    use_blender = False

if not use_blender:
    input()