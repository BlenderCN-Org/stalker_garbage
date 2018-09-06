import bpy, random, time
from . import xray_utils


def random_material_color(object):
    for material_slot in object.material_slots:
        material_slot.material.diffuse_color = (random.random(),
                                                random.random(),
                                                random.random())


def assign_materials(object, material_indices, matSlots):
    for n, material in enumerate(material_indices):
        index = matSlots[material]
        object.data.polygons[n].material_index = index


def create_materials(mesh, materials, som_property):
    matSlots = {}
    for n, i in enumerate(materials):
        material = bpy.data.materials.new('material_{:0>2}'.format(i))
        mesh.materials.append(material)
        matSlots[i] = n
        if som_property:
            material.xray_2_sided = som_property[n][0]
            material.xray_occ = som_property[n][1]
    return matSlots


def create_uvs(mesh, uvs):
    mesh.uv_textures.new()
    uv_layer = mesh.uv_layers.active.data
    for tris in mesh.polygons:
        for loop_index in range(tris.loop_start, tris.loop_start + tris.loop_total):
            vertex_index = mesh.loops[loop_index].vertex_index
            uv_layer[loop_index].uv = (uvs[vertex_index])


def create_texture(object, image_name, ext='dds'):
    path = bpy.context.scene.stalkerTexturesDir
    material = bpy.data.materials.new(image_name + '_Mat')
    object.data.materials.append(material)
    material.specular_intensity = 0
    image = bpy.data.images.load(path + image_name + '.' + ext)
    texture = bpy.data.textures.new(image_name + '_Tex', type = 'IMAGE')
    texture.image = image
    tex_slot = object.material_slots[0].material.texture_slots.add()
    tex_slot.texture = texture
    tex_slot.texture_coords = 'UV'
    for i in object.data.uv_textures[0].data:
        i.image = image


def create_object(name='xray_object'):
    object = bpy.data.objects.new(name, bpy.data.meshes.new(name + '_mesh'))
    bpy.context.scene.objects.link(object)
    return object


def create_mesh(meshData):
    verts = meshData.get('verts')
    faces = meshData.get('faces')
    materials = meshData.get('materials')
    material_indices = meshData.get('material_indices')
    uvs = meshData.get('uvs')
    images = meshData.get('images')
    som_property = meshData.get('som_property')
    object = create_object()
    mesh = object.data
    if not faces:
        faces = ()
    mesh.from_pydata(verts, (), faces)
    if materials:
        matSlots = create_materials(mesh, materials, som_property)
        random_material_color(object)
    if material_indices:
        assign_materials(object, material_indices, matSlots)
    if uvs:
        create_uvs(mesh, uvs)
    if images:
        create_texture(object, images)


def parse_file(file_data, ext):
    if ext == 'cform':
        from . import parse_cform
        mesh_data = parse_cform.parse_main(file_data)
        return mesh_data
    elif ext == 'details':
        from . import parse_details
        mesh_data = parse_details.parse_main(file_data)
        return None
    elif ext == 'dm':
        from . import parse_dm
        mesh_data = parse_dm.parse_main(file_data)
        return mesh_data
    elif ext == 'hom':
        from . import parse_hom
        mesh_data = parse_hom.parse_main(file_data)
        return mesh_data
    elif ext == 'wallmarks':
        from . import parse_wallmarks
        mesh_data = parse_wallmarks.parse_main(file_data)
        return None
    elif ext == 'ogf':
        from . import parse_ogf
        mesh_data = parse_ogf.parse_main(file_data)
        return None
    elif ext == 'object':
        from . import parse_object
        mesh_data = parse_object.parse_main(file_data)
        return mesh_data
    elif ext == 'som':
        from . import parse_som
        mesh_data = parse_som.parse_main(file_data)
        return mesh_data


def import_file(absolute_path):
    startTime = time.time()
    ext = absolute_path.split('.')[-1]
    name = absolute_path.split('\\')[-1][0 : -(len(ext)+1)]
    path = absolute_path[:-(len(name) + len(ext) + 1)]
    file_data = xray_utils.read_bin_file(name, ext, path)
    mesh_data = parse_file(file_data, ext)
    if mesh_data:
        create_mesh(mesh_data)
    print('{:.6}s'.format(time.time() - startTime))

