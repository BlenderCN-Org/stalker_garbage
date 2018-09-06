import bpy, time
from struct import pack as p


def export_som(mesh, path, use2sided=False):
    f = open(path, 'wb')
    f.write(p('III', 0x0, 4, 0))    # version block
    f.write(p('II', 0x1, len(mesh.polygons) * 44))  # polygons block
    two_sided, occ = int(use2sided), 0.0
    for polygon in mesh.polygons:
        v1x, v1y, v1z = mesh.vertices[polygon.vertices[0]].co.xzy
        v2x, v2y, v2z = mesh.vertices[polygon.vertices[2]].co.xzy
        v3x, v3y, v3z = mesh.vertices[polygon.vertices[1]].co.xzy
        tris = p('9f', v1x, v1y, v1z, v2x, v2y, v2z, v3x, v3y, v3z)
        option = p('If', two_sided, occ)
        f.write(tris + option)
    f.close()


stime = time.time()
mesh = bpy.context.object.data
export_som(mesh, 'c:\\level.som')
ftime = time.time()
print('{0: <32} time: {1:.6}s'.format(mesh.name, ftime - stime))

