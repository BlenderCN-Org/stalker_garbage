import bpy
from struct import pack as p


def export_som(ob, path):
    mesh = ob.data
    f = open(path, 'wb')
    f.write(p('III', 0x0, 4, 0))    # version block
    f.write(p('II', 0x1, len(mesh.polygons) * 44))  # polygons block
    for polygon in mesh.polygons:
        v1x, v1y, v1z = mesh.vertices[polygon.vertices[0]].co.xzy
        v2x, v2y, v2z = mesh.vertices[polygon.vertices[2]].co.xzy
        v3x, v3y, v3z = mesh.vertices[polygon.vertices[1]].co.xzy
        tris = p('9f', v1x, v1y, v1z, v2x, v2y, v2z, v3x, v3y, v3z)
        mat = ob.material_slots[polygon.material_index].material
        option = p('If', mat.xray_2_sided, mat.xray_occ)
        f.write(tris + option)
    f.close()

