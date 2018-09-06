bl_info = {'name':     'X-Ray SOM',
           'author':   'Pavel_Blend',
           'version':  (0, 0, 0),
           'blender':  (2, 7, 1),
           'category': 'Import-Export',
           'location': 'Scene properties, Material properties',
           'description': 'Import/Export *.som mesh',
           'wiki_url': '',
           'tracker_url': '',
           'warning': ''}

import bpy, time
from bpy.props import *
from . import export_som
from bpy_extras.io_utils import ExportHelper


export_path = 'x:\\import\\blender_export\\'
tScn = bpy.types.Scene
tMat = bpy.types.Material

tMat.xray_occ = FloatProperty(name='Sound Occlusion',
                              default=0,
                              min=0,
                              max=1,
                              description = 'X-Ray SDK > Shader Editor > '\
                              'Material > Item Properties > '\
                              'Factors > Sound Occlusion')

tMat.xray_2_sided = BoolProperty(name='2 Sided',
                                 description = 'X-Ray SDK > Actor Editor > '\
                                 'Surfaces > Surface > 2 Sided')

tScn.xray_export_objects = EnumProperty(items=[
                     ('SELECT', 'Select', 'Export select objects to *.som'),
                     ('ACTIVE', 'Active', 'Export active object to *.som'),
                     ('ALL', 'All', 'Export all scene objects to *.som')],
                     name='Export Objects')

tScn.xray_export_som_path = StringProperty(name='Export Path',
                                           default=export_path,
                                           description = 'Export *.som path',
                                           subtype = 'FILE_PATH')


def export_object_to_som(ob, path, add_name=True):
    stime = time.time()
    scn = bpy.context.scene
    for i in scn.objects:
        i.select = False
    me = ob.to_mesh(scn, True, 'PREVIEW', calc_tessface=False)
    temp_object = bpy.data.objects.new('TEMP', me)
    scn.objects.link(temp_object)
    temp_object.select = True
    bpy.context.scene.objects.active = temp_object
    temp_object.location = ob.location
    temp_object.rotation_mode = 'XYZ'
    temp_object.rotation_euler = ob.rotation_euler
    temp_object.scale = ob.scale
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.quads_convert_to_tris()
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    if add_name:
        export_som.export_som(temp_object, path + ob.name + '.som')
    else:
        export_som.export_som(temp_object, path)
    bpy.context.scene.objects.unlink(temp_object)
    me.user_clear()
    bpy.data.meshes.remove(me)
    ftime = time.time()
    print('EXPORT: {0: <32} time: {1:.6}s'.format(ob.name, ftime - stime))
    return {'FINISHED'}


class Stalker_Material_Panel_SOM(bpy.types.Panel):
    bl_label = 'S.T.A.L.K.E.R. Tools'
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    @classmethod
    def poll(cls, context):
        return context.material

    def draw(self, context):
        layout = self.layout
        ob = bpy.context.object
        mat = ob.active_material
        layout.label('Sound Occluder Mesh (level.som)')
        layout.prop(mat, 'xray_2_sided')
        layout.prop(mat, 'xray_occ')


class Stalker_Scene_Panel_SOM(bpy.types.Panel):
    bl_label = 'S.T.A.L.K.E.R. Tools'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'

    def draw(self, context):
        scn = bpy.context.scene
        layout = self.layout
        layout.label('Sound Occluder Mesh (level.som)')
        layout.prop(scn, 'xray_export_objects')
        layout.prop(scn, 'xray_export_som_path')
        layout.operator('stalker_tools.export_som', text='EXPORT *.SOM')


class Stalker_Export_SOM(bpy.types.Operator):
    bl_idname = 'stalker_tools.export_som'
    bl_label = 'Export *.SOM (X-Ray)'

    def execute(self, context):
        path = bpy.context.scene.xray_export_som_path
        print('RUN EXPORT (DIR: {})'.format(path))
        scn = bpy.context.scene
        if scn.xray_export_objects == 'SELECT':
            obs = bpy.context.selected_objects
            if len(obs) > 0:
                for ob in obs:
                    if len(ob.material_slots) != 0:
                        export_object_to_som(ob, path)
                    else:
                        self.report({'ERROR'}, \
                        'Object \'{}\' not have material!'.format(ob.name))
            else:
                self.report({'ERROR'}, 'Selected objects is None!')
        if scn.xray_export_objects == 'ACTIVE':
            ob = bpy.context.active_object
            if ob:
                if len(ob.material_slots) != 0:
                    export_object_to_som(ob, path)
                else:
                    self.report({'ERROR'}, \
                    'Object \'{}\' not have material!'.format(ob.name))
            else:
                self.report({'ERROR'}, 'Active object is None!')
        if scn.xray_export_objects == 'ALL':
            if len(scn.objects) > 0:
                for ob in scn.objects:
                    if len(ob.material_slots) != 0:
                        export_object_to_som(ob, path)
                    else:
                        self.report({'ERROR'}, \
                        'Object \'{}\' not have material!'.format(ob.name))
            else:
                self.report({'ERROR'}, 'Scene not have objects!')
        return {'FINISHED'}


class Stalker_Export_Som_Menu(bpy.types.Operator, ExportHelper):
    bl_idname = "stalker_tools.export_som_menu"
    bl_description = 'Export from SOM file format (.som)'
    bl_label = "Export SOM"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    filename_ext = ".som"
    filter_glob = StringProperty(default="*.som", options={'HIDDEN'})

    filepath = bpy.props.StringProperty(
        name="File Path", 
        description="File path used for exporting the SOM file", 
        maxlen= 1024, default= "")

    def execute(self, context):
        ob = bpy.context.object
        if ob:
            if len(ob.material_slots) != 0:
                export_object_to_som(ob, self.properties.filepath, add_name=False)
            else:
                self.report({'ERROR'}, \
                'Object \'{}\' not have material!'.format(ob.name))
        else:
            self.report({'ERROR'}, 'Active object is None!')
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


def menu_func_export(self, context):
    self.layout.operator(Stalker_Export_Som_Menu.bl_idname,
                         text="Sound Occluder Mesh (.som)")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)


if __name__ == '__main__':
    register()

