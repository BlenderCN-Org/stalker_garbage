use_blender = True
try:
    import bpy
except:
    use_blender = False

def crete_mesh(name, vertices, uvs, triangles, texture_name):
    if use_blender:
        mesh = bpy.data.meshes.new(name + '_Mesh')
        object = bpy.data.objects.new(name, mesh)
        scene = bpy.context.scene
        scene.objects.link(object)
        mesh.from_pydata(vertices, (), triangles)
        mesh.uv_textures.new()
        uv_layer = mesh.uv_layers.active.data
        for tris in mesh.polygons:
            for loop_index in range(tris.loop_start, tris.loop_start + tris.loop_total):
                vertex_index = mesh.loops[loop_index].vertex_index
                uv_layer[loop_index].uv = (uvs[vertex_index])
    else:
        pass
