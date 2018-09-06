import bpy

def export_uv(mesh):
    uvs = []
    
    uv_layer = mesh.uv_layers[0]
    for triangle in mesh.polygons:
        for i in triangle.loop_indices:
            lookupIndex = mesh.loops[i].vertex_index
            uvCoord = uv_layer.data[i].uv
            uvs.append([uvCoord[0], 1 - uvCoord[1]])
    
    return uvs