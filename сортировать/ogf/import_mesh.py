def crete_mesh(name, vertices, uvs, triangles, texture_name):
    import ogf_prop

    use_blender = True
    try:
        import bpy
    except:
        use_blender = False
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
        material = bpy.data.materials.new(texture_name + '_Mat')
        bpy.context.scene.objects.active = object
        bpy.ops.object.material_slot_add()
        object.material_slots[0].material = material
        material.specular_intensity = 0
        image = bpy.data.images.load(ogf_prop.image_path + texture_name + '.' + ogf_prop.image_ext)
        texture = bpy.data.textures.new(texture_name + '_Tex', type = 'IMAGE')
        texture.image = image
        tex_slot = object.material_slots[0].material.texture_slots.add()
        tex_slot.texture = texture
        tex_slot.texture_coords = 'UV'
        
        for i in object.data.uv_textures[0].data:
            i.image = image
    else:
        pass
