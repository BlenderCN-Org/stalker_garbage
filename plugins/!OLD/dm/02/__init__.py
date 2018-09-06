bl_info = {
    'name': 'Import *.dm',
    'author': 'Pavel Blend',
    'version': (0, 0, 0),
    'blender': (2, 7, 1),
    'description': 'Import STALKER (SOC) *.dm model',
    'warning': '',
    'support': 'COMMUNITY',
    'category': 'Import-Export'}

import bpy
from io_mesh_dm import dm_read


def register():
    bpy.utils.register_module(__name__)
 
def unregister():
    bpy.utils.unregister_module(__name__)
 
if __name__ == "__main__":
    register()