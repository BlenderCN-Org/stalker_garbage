def crete_mesh(vertices):
    # delete this module (temp)
    
    use_blender = True
    try:
        import bpy
    except:
        use_blender = False
    if use_blender:
        mesh = bpy.data.meshes.new('_Mesh')
        object = bpy.data.objects.new('name', mesh)
        scene = bpy.context.scene
        scene.objects.link(object)
        mesh.from_pydata(vertices, (), ())

