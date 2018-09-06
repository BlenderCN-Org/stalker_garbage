import bpy, utils, parse_cform, import_utils, time
from utils import unpack_data as u

start_time = time.time()
data = utils.read_bin_file('level', 'cform', 'c:\\')
verts, faces, material_indices, materials = parse_cform.parse_cform(data)
import_utils.crete_mesh(verts, faces, materials, material_indices)
finish_time = time.time()
print('total time: {:.5}s'.format(finish_time-start_time))