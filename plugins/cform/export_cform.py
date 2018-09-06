bl_info = {'name'        : 'Export CFORM',
           'author'      : 'Pavel_Blend',
           'version'     : (0, 0, 0),
           'blender'     : (2, 7, 1),
           'category'    : 'Import-Export',
           'location'    : 'Scene properties',
           'support'     : 'COMMUNITY',
           'description' : 'Import X-Ray Engine level collision form mesh'}


import bpy, time
from struct import pack as p
from bpy.props import StringProperty


bpy.types.Scene.exportCformDir = StringProperty(name='Export Path',
                                                default = 'c:\\',
                                                subtype = 'FILE_PATH')


class ExportCformPanel(bpy.types.Panel):
    bl_label = 'Export CForm'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        layout.prop(scn, 'exportCformDir')
        layout.operator('cform.export', text='Export')


class ExportCform(bpy.types.Operator):
    bl_idname = 'cform.export'
    bl_label = 'Export CForm'


    def execute(self, context):
        startTime = time.time()
        path = bpy.context.scene.exportCformDir
        path = path.encode(encoding='cp1251')
        f = open(path + b'level.cform', 'wb')
        f.write(b'\x04\x00\x00\x00')
        me = context.scene.objects.active.data
        vertCnt = len(me.vertices)
        triCnt = len(me.polygons)
        f.write(p('II', vertCnt, triCnt))
        f.write(p('6f', -100, -100, -100, 100, 100, 100))
        for v in me.vertices:
            f.write(p('3f', v.co.x, v.co.z, v.co.y))
        gameMtl = []
        for mat in context.scene.objects.active.data.materials:
            gameMtl.append(mat.stalkerMatID)
        ob = context.scene.objects.active
        for face in me.polygons:
            f.write(p('III', face.vertices[0], face.vertices[2], face.vertices[1]))
            vertID = face.vertices[0]
            vertex = me.vertices[vertID]
            if len(vertex.groups) == 1:
                groupID = vertex.groups[0].group
                vertexGroup = ob.vertex_groups[groupID]
                vertexGroupName = vertexGroup.name
                sectorID = int(vertexGroupName)
            else:
                vertID = face.vertices[1]
                vertex = me.vertices[vertID]
                if len(vertex.groups) == 1:
                    groupID = vertex.groups[0].group
                    vertexGroup = ob.vertex_groups[groupID]
                    vertexGroupName = vertexGroup.name
                    sectorID = int(vertexGroupName)
                else:
                    vertID = face.vertices[2]
                    vertex = me.vertices[vertID]
                    if len(vertex.groups) == 1:
                        groupID = vertex.groups[0].group
                        vertexGroup = ob.vertex_groups[groupID]
                        vertexGroupName = vertexGroup.name
                        sectorID = int(vertexGroupName)
            f.write(p('HH', gameMtl[face.material_index] | 0xc000, sectorID))
        print('total time: {0:.6}'.format(time.time() - startTime))
        f.close()
        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == '__main__':
    register()

